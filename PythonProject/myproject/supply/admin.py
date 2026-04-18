from django.contrib import admin
from .models import Ingredient, Inventory, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'delivery_details')
    search_fields = ('name', 'contact_info', 'delivery_details')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity_unit', 'reorder_threshold', 'storage_condition', 'storage_area', 'supplier')
    list_filter = ('storage_condition', 'storage_area', 'supplier')
    search_fields = ('name', 'supplier__name')


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'quantity_available', 'expiry_date', 'location')
    list_filter = ('location',)
    search_fields = ('ingredient__name', 'location')
