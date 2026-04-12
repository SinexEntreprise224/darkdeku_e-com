from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from store.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),

    # --- Auth ---
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    # --- Boutique & Panier ---
    path('detail/<slug:slug>/', detail, name='detail'),
    path('order/<slug:slug>/', order, name='order'),
    path('cart/', cart, name='cart'),
    path('add_to_cart/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('empty-cart/', empty_cart, name='empty_cart'),
    path('cart/leave_to_cart/<slug:slug>', leave_to_cart, name='leave_to_cart'),

    # --- Catégories ---
    path('category/all/', all_categories, name='all_categories'),
    path('category/add/', add_category, name='add_category'),
    path('category/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),

    # --- Produits ---
    path('product/all/', all_products, name='all_products_list'),
    path('product/add/', add_product, name='add_product'),
    path('product/edit/<slug:slug>/', edit_product, name='edit_product'),
    path('product/delete/<slug:slug>/', delete_product, name='delete_product'),
    path('search/<str:category_name>/', search_products_by_name_and_category, name='search'),

    # --- Order ---
    path('order/<slug:slug>/', order, name='order'),
    path('oder/edit/<int:order_id>/', edit_order, name='edit_order'),

    # --- Filtres ---
    path('product/category/<int:category_id>/', product_by_category, name='product_by_category'),
    path('product/make/<int:make_id>/', product_by_make, name='product_by_make'),
    path('product/tag/<int:tag_id>/', product_by_tag, name='product_by_tag'),

    # --- Marques (Make) ---
    path('make/all/', all_makes, name='all_makes'),
    path('make/add/', add_make, name='add_make'),
    path('make/edit/<int:make_id>/', edit_make, name='edit_make'),
    path('make/delete/<int:make_id>/', delete_make, name='delete_make'),

    # --- Tags ---
    path('tag/all/', all_tags, name='all_tags'),
    path('tag/add/', add_tag, name='add_tag'),
    path('tag/edit/<int:tag_id>/', edit_tag, name='edit_tag'),
    path('tag/delete/<int:tag_id>/', delete_tag, name='delete_tag'),

    # --- Admin ---
    path('dashboard/index', admin_index, name='admin_index'),
    path('dashboard/delete_user/<int:user_id>/', delete_user, name='delete_user'),

    # --- user ---
    path('user/edit', edit_user, name='edit_profile'),
    path('user/index', profile, name='profile'),
    path('user/delete_account', delete_account, name='delete_account'),
    path('user/edit_password', edit_password, name='edit_password'),
    path('user/order', load_orders, name='all_orders')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)