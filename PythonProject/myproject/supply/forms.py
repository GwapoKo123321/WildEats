from django import forms
from django.contrib.auth.models import User

from .models import Ingredient, Inventory, Supplier


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["ingredient_id", "name", "contact_info", "rating", "delivery_frequency"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "recipe_id",
            "inventory_id",
            "notification_id",
            "name",
            "quantity_unit",
            "threshold",
            "storage_condition",
            "expiry_date",
            "supplier",
        ]
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = [
            "cafeteria_id",
            "ingredient",
            "notification_id",
            "quantity_available",
            "expiration_date",
            "location",
        ]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }
