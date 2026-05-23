from django.contrib import admin
from .models import Ingredient, Inventory, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('ingredient_id', 'name', 'contact_info', 'rating', 'delivery_frequency')
    list_filter = ('rating', 'delivery_frequency')
    search_fields = ('name', 'contact_info')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'quantity_unit',
        'threshold',
        'storage_condition',
        'expiry_date',
        'supplier',
        'recipe_id',
        'inventory_id',
        'notification_id',
    )
    list_filter = ('quantity_unit', 'storage_condition', 'supplier')
    search_fields = ('name', 'supplier__name')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'cafeteria_id',
        'quantity_available',
        'expiration_date',
        'location',
        'notification_id',
    )
    list_filter = ('location',)
    search_fields = ('ingredient__name', 'location')
