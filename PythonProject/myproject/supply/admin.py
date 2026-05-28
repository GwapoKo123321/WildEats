from django.contrib import admin
from .models import (
    Cafeteria,
    Ingredient,
    IngredientInventory,
    IngredientNotification,
    IngredientSupplier,
    Inventory,
    InventoryNotification,
    Notification,
    Recipe,
    RecipeIngredient,
    Supplier,
)


class IngredientSupplierInline(admin.TabularInline):
    model = IngredientSupplier
    extra = 1


class IngredientInventoryInline(admin.TabularInline):
    model = IngredientInventory
    extra = 1


class IngredientNotificationInline(admin.TabularInline):
    model = IngredientNotification
    extra = 1


class InventoryNotificationInline(admin.TabularInline):
    model = InventoryNotification
    extra = 1


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'operating_hours', 'capacity')
    search_fields = ('name', 'location')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('date', 'view_status')
    list_filter = ('view_status', 'date')
    inlines = (IngredientNotificationInline, InventoryNotificationInline)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'preparation_time')
    search_fields = ('instructions',)
    inlines = (RecipeIngredientInline,)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_info', 'rating', 'delivery_frequency')
    list_filter = ('rating',)
    search_fields = ('name', 'contact_info')
    inlines = (IngredientSupplierInline,)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'quantity_unit',
        'threshold',
        'storage_condition',
        'expiry_date',
        'supplier_names',
    )
    list_filter = ('quantity_unit', 'storage_condition', 'suppliers')
    search_fields = ('name', 'suppliers__name')
    inlines = (IngredientSupplierInline, IngredientInventoryInline, IngredientNotificationInline, RecipeIngredientInline)

    @admin.display(description='Suppliers')
    def supplier_names(self, obj):
        return ', '.join(supplier.name for supplier in obj.suppliers.all())


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        'cafeteria',
        'ingredient_names',
        'quantity_available',
        'expiration_date',
        'location',
    )
    list_filter = ('cafeteria', 'location')
    search_fields = ('ingredients__name', 'location', 'cafeteria__name')
    inlines = (IngredientInventoryInline, InventoryNotificationInline)

    @admin.display(description='Ingredients')
    def ingredient_names(self, obj):
        return ', '.join(ingredient.name for ingredient in obj.ingredients.all())
