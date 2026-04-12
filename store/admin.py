from django.contrib import admin
from store.models import Product, User, Category, Make, Tag, Order

# Enregistrement simple pour l'utilisateur
admin.site.register(User)


# Configuration pour les Catégories
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    search_fields = ('product__name',)


# Configuration pour les Marques (Make)
@admin.register(Make)
class MakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_partner', 'created_at')
    list_filter = ('is_partner', 'created_at', 'updated_at')
    search_fields = ('name',)


# Configuration pour les Tags
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# Configuration pour les Produits
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Le slug se base uniquement sur le nom pour éviter les erreurs de type
    prepopulated_fields = {"slug": ("name",)}

    # Liste les colonnes à afficher
    list_display = ('name', 'price', 'quantity', 'category', 'make', 'is_active','created_at')

    # Filtres latéraux
    list_filter = ('category', 'make', 'created_at')

    # Barre de recherche
    search_fields = ('name', 'description')

    # Pour gérer les relations ManyToMany (Tags) plus proprement
    filter_horizontal = ('tags',)