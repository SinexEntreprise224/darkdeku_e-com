from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_user, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from store.decorators import admin_required
from store.forms import SignupForm, LoginForm, CategoryForm, ProductForm, MakeForm, TagForm, EditUserProfileForm, \
    EditPasswordForm
from django.db.models import Sum, F
from store.models import Product, Order, Cart, Category, Make, Tag, User

# Create your views here.

def index(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "home.html", context={"products": products, 'categories': categories})

def error_404(request, exception=None):
    return render(request, '404.html', status=404)

# --- Auth ---
def login(request):
   if request.method == "POST":
       form = LoginForm(request, data=request.POST)
       if form.is_valid():
           username = form.cleaned_data.get("username")
           password = form.cleaned_data.get("password")
           user = authenticate(username=username, password=password)
           if user is not None:
               auth_user(request, user)
               messages.success(request, "Connexion réussie!")
               next_url = request.POST.get("next")
               if next_url:
                  return redirect(next_url)
               return redirect("index")
           else:
               form = LoginForm()
               return render(request, "auth/login.html", {"form": form})
       messages.error(request, "Une erreur est survenue")
       form = LoginForm(request)
       return render(request, "auth/login.html", {"form": form})

   else:
       form = LoginForm()
       return render(request, "auth/login.html", {"form": form})

def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription réussie!")
            return redirect('login')

        messages.error(request, "Une erreur est survenue")
        return render(request, "auth/register.html", {"form": form})
    else:
        form = SignupForm()
        return render(request, "auth/register.html", {"form": form})

def logout(request):
    auth_logout(request)
    messages.info(request, "au plaisir de vous révoir!")
    return redirect("index")

# --- catalogue ---
@login_required()
def all_categories(request):
    if request.user.role != 'admin':
        messages.error(request, "Vous n'avez pas accès à cette page")
        return redirect("index")
    categories = Category.objects.all()
    return render(request, "category/all.html", {"categories": categories})

@login_required
def add_category(request):
    if request.user.role != 'admin':
        messages.error(request, "Tu n'as pas les droits pour accéder à cette page.")
        return redirect("index")

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Catégorie ajoutée avec succès !")
            return redirect("index")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CategoryForm()

    return render(request, "category/add.html", {"form": form})

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.user.role != 'admin':
        messages.error(request, "Accès refusé.")
        return redirect("index")

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "La catégorie a été mise à jour !")
            return redirect("index")
    else:
        form = CategoryForm(instance=category)

    return render(request, "category/edit.html", {"form": form, "category": category})

@login_required
def delete_category(request, category_id):
    if request.user.role != 'admin':
        messages.error(request, "Accès refusé !")
        return redirect("index")

    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        category.delete()
        messages.success(request, "La catégorie a été supprimée définitivement.")
        return redirect("category") # On retourne à la liste

    return render(request, "category/delete_cofirmation.html", {"category": category})


# --- product ---
@login_required
def all_products(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "product/all.html", {"products": products})

def detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("index")
    return render(request, "product/detail.html", context={"product": product})


def search_products_by_name_and_category(request, category_name):
    query = request.GET.get('q', '')
    category = get_object_or_404(Category, name=category_name)

    if query:
        products = Product.objects.filter(
            name__icontains=query,
            category=category
        )
    else:
        products = Product.objects.filter(category=category)

    return render(request, "product/search.html", {
        "products": products,
        "query": query,
        "category": category
    })


@login_required
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Produit ajouté avec succès!')
            return redirect("index")
        messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = ProductForm()
    return render(request, "product/add.html", {"form": form})

@login_required
@admin_required
def edit_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("index")
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations de ce produit ont bien été mise à jour !")
            return redirect("index")
        else:
            return render(request, "product/edit.html", {"form": form, "product": product})
    else:
        form = ProductForm(instance=product)
        return render(request, "product/edit.html", {"form": form})

@login_required
@admin_required
def delete_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.is_active = False
        product.save()
        messages.success(request, "Produit supprimé avec succès !")
        return redirect("index")
    return render(request, "product/delete.html", {"product": product})

def product_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, "product/category.html", {"products": products, "category": category})

def product_by_make(request, make_id):
    make = get_object_or_404(Make, pk=make_id)
    products = Product.objects.filter(make=make, is_active=True)
    return render(request, "product/make.html", {"products": products, "make": make})

def product_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    products = Product.objects.filter(tags=tag, is_active=True)
    return render(request, "product/tag.html", {"products": products, "tag": tag})

# --- cart ---

@login_required
def add_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("index")
    cart_, _ = Cart.objects.get_or_create(user=user)

    order_, created = Order.objects.get_or_create(
        user=user,
        product=product,
        ordered=False,
        defaults={'quantity': 1}
    )

    if created:
        cart_.orders.add(order_)
        messages.success(request, "Le produit a été ajouté au panier.")
        return redirect("cart")
    else:
        order_.quantity += 1
        order_.save()
        messages.info(request, "La quantité a été mise à jour.")

        return redirect("cart")

@login_required
def cart(request):
    user = request.user
    cart_, _ = Cart.objects.get_or_create(user=user)
    orders = cart_.orders.filter(ordered=False)
    total = sum(order_.quantity * order_.product.price for order_ in orders)
    return render(request, "cart.html", {"orders": orders, "total": total})


@login_required
def leave_to_cart(request, slug):
    user = request.user
    product = get_object_or_404(Product, slug=slug)
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("cart")
    cart_= get_object_or_404(Cart, user=user)

    order_ = Order.objects.filter(
        user=user,
        product=product,
        ordered=False
    ).first()

    if order_:
        # 4. On retire la commande du panier et on la supprime
        cart_.orders.remove(order_)
        order_.delete()
        messages.success(request, f"{product.name} a été retiré de ton panier.")
    else:
        messages.info(request, "Ce produit n'était pas dans ton panier.")

    # 5. On redirige vers le panier
    return redirect("cart")

@login_required
def empty_cart(request):
    user = request.user
    cart_ = Cart.objects.filter(user=user).first()

    if cart_:
        cart_.orders.filter(ordered=False).delete()

        cart_.orders.clear()

        messages.success(request, "Ton panier a été vidé avec succès.")
    else:
        messages.info(request, "Ton panier était déjà vide.")

    return redirect("index")

# --- order ---
@login_required
def order(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("index")
    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity"))
        except (ValueError, TypeError):
            messages.error(request, "Quantité invalide.")
            return redirect("order", slug=slug)

        if quantity > product.quantity or quantity <= 0:
            messages.error(request, f"Désolé, seulement {product.quantity} articles en stock.")
            return redirect("order", slug=slug)

        ordered, created = Order.objects.get_or_create(
            user=request.user,
            product=product,
            ordered=False,
            defaults={'quantity': quantity}
        )

        if not created:
            ordered.quantity = quantity

        ordered.ordered = True
        ordered.save()

        product.quantity -= quantity
        product.save()

        messages.success(request, "La commande a bien été lancée !")
        return redirect("index")

    else:
        return render(request, "order/order.html", {"product": product})


@login_required
def edit_order(request, order_id):
    order_ = get_object_or_404(Order, pk=order_id, user=request.user)
    product = order_.product
    if  not product.is_active:
        messages.error(request, "ce produit n'existe pas")
        return redirect("index")
    if order_.ordered:
        messages.error(request, "Impossible de modifier une commande déjà validée.")
        return redirect("cart")

    if request.method == "POST":
        try:
            new_quantity = int(request.POST.get("quantity"))
        except (ValueError, TypeError):
            messages.error(request, "Quantité invalide.")
            return redirect("cart")

        if new_quantity > order_.product.quantity:
            messages.error(request, f"Stock insuffisant (Max: {order_.product.quantity})")
            return redirect("cart")

        if new_quantity <= 0:
            order_.delete()
            messages.info(request, "Article retiré du panier.")
        else:
            order_.quantity = new_quantity
            order_.save()
            messages.success(request, "Quantité mise à jour !")

        return redirect("cart")  # Rediriger vers le panier est plus logique ici

    return render(request, "order/edit.html", {"order": order_, "product": product})

@login_required
def delete_order(request, order_id):
    order_ = get_object_or_404(Order, pk=order_id, user=request.user)
    if  not order_.ordered:
        order_.delete()
        messages.success(request, "Commande supprimé avec succès!")
        return redirect("cart")
    else:
        messages.error(request, "Impossible de supprimer un produit commandé!")
        return redirect("cart")

# --- Make ---
@login_required
@admin_required
def all_makes(request):

    makes = Make.objects.all().order_by('name')
    return render(request, "make/all.html", {"makes": makes})


@login_required
@admin_required
def add_make(request):

    if request.method == "POST":
        form = MakeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"La marque {form.cleaned_data['name']} a été ajoutée !")
            return redirect("all_makes")
        else:
            messages.error(request, "Erreur lors de l'ajout.")
    else:
        form = MakeForm()

    return render(request, "make/add.html", {"form": form})


@login_required
@admin_required
def edit_make(request, make_id):
    make = get_object_or_404(Make, pk=make_id)

    if request.method == 'POST':
        form = MakeForm(request.POST, instance=make)
        if form.is_valid():
            form.save()
            messages.success(request, f"La marque {make.name} a été mise à jour.")
            return redirect("all_makes")
    else:
        form = MakeForm(instance=make)

    return render(request, "make/edit.html", {"form": form, "make": make})

@login_required
@admin_required
def delete_make(request, make_id):
    make = get_object_or_404(Make, pk=make_id)

    if request.method == "POST":
        make.delete()
        messages.success(request, "La marque a été supprimée.")
        return redirect("all_makes")

    return render(request, "make/delete_confirmation.html", {"make": make})

# --- Tags ---
@login_required
@admin_required
def all_tags(request):
    if request.user.role != 'admin':
        messages.error(request, "Accès refusé.")
        return redirect("index")
    tags = Tag.objects.all().order_by('name')
    return render(request, "tag/all.html", {"tags": tags})

@login_required
@admin_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag ajouté !")
            return redirect("all_tags")
    else:
        form = TagForm()
    return render(request, "tag/add.html", {"form": form})

@login_required
@admin_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)

    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag mis à jour.")
            return redirect("all_tags")
    else:
        form = TagForm(instance=tag)
    return render(request, "tag/edit.html", {"form": form, "tag": tag})

@login_required
@admin_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    if request.method == "POST":
        tag.delete()
        messages.success(request, "Tag supprimé.")
        return redirect("all_tags")
    return render(request, "tag/delete_confirmation.html", {"tag": tag})

# --- Admin
@login_required
@admin_required
def admin_index(request):
    products = Product.objects.filter(is_active=True)
    tags = Tag.objects.all()
    makes = Make.objects.all()
    categories = Category.objects.all()
    orders = Order.objects.all()
    users = User.objects.filter(role='user', is_active=True).annotate(
        total_spent=Sum(F('order__quantity') * F('order__product__price'))
    )
    return render(request, "admin/index.html", {
        "products": products,
        "tags": tags,
        "makes": makes,
        "categories": categories,
        "orders": orders,
        "users": users,
    })

@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.role != 'admin' or user == request.user:
        messages.error(request, "Impossible de continuer l'action!")
        return redirect("admin_index")

    if request.method == "POST":
        user.is_active = False
        user.save()
        messages.success(request, "Utilisateur supprimée avec succès!")
        return redirect("admin_index")
    else:
        return render(request, "admin/delete_user_confirmation.html", {"user": user})

# --- User ---
@login_required
def edit_user(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == "POST":
        form = EditUserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations de votre compte ont été modifiées!")
            if user.role == 'admin':
                return redirect("admin_index")
            return redirect('index')
        messages.error(request,"Quelque chose s'est mal passé, veuillez résoudre les problèmes ci-desssous!")
        return redirect('edit_user')
    else:
        form = EditUserProfileForm(instance=user)
        return render(request, "user/edit.html", {"form": form})

@login_required
def profile(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, "user/index.html", {"user": user})

@login_required
def delete_account(request):
    user = get_object_or_404(User, id=request.user.id)
    if user.role == 'admin':
        messages.error(request, "Un administrateur ne peut supprimer son compte !")
        return redirect('profile')
    if request.method == "POST":
        user.delete()
        messages.success(request, "Merci et au revoir!")
        return redirect("index")
    return render(request, "user/delete_confirmation.html", {"user": user})

@login_required
def edit_password(request):
    if request.method == "POST":
        form = EditPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Mot de passe modifié avec succès !")
            return redirect("profile")

        messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = EditPasswordForm(user=request.user)

    return render(request, "user/edit_password.html", {"form": form})

@login_required
def load_orders(request):
    orders = Order.objects.filter(user=request.user)
    status = "Confirmée" if orders.ordered else "En attente"
    return render(request, "order/all.html", {"orders": orders, "status": status})
