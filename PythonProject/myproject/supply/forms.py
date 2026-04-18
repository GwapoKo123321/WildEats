from django import forms

from .models import Ingredient, Inventory, Supplier


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_info", "delivery_details"]


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "quantity_unit",
            "reorder_threshold",
            "storage_condition",
            "storage_area",
            "supplier",
        ]


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ["ingredient", "quantity_available", "expiry_date", "location"]
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }
