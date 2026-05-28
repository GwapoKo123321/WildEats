from django import forms
from django.contrib.auth.models import User

from .models import Ingredient, Inventory, Notification, Recipe, Supplier


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ["name", "contact_info", "rating", "delivery_frequency"]


class IngredientForm(forms.ModelForm):
    suppliers = forms.ModelMultipleChoiceField(
        queryset=Supplier.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
    )
    recipes = forms.ModelMultipleChoiceField(
        queryset=Recipe.objects.order_by("id"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )
    notifications = forms.ModelMultipleChoiceField(
        queryset=Notification.objects.order_by("-date", "-id"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Ingredient
        fields = [
            "name",
            "quantity_unit",
            "threshold",
            "storage_condition",
            "expiry_date",
            "suppliers",
            "recipes",
            "notifications",
        ]
        widgets = {
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        ingredient = super().save(commit=commit)
        if commit:
            ingredient.suppliers.set(self.cleaned_data["suppliers"])
            ingredient.recipes.set(self.cleaned_data["recipes"])
            ingredient.notifications.set(self.cleaned_data["notifications"])
        else:
            self.save_m2m = self._save_m2m_for_unsaved_ingredient(ingredient)
        return ingredient

    def _save_m2m_for_unsaved_ingredient(self, ingredient):
        def save_m2m():
            ingredient.suppliers.set(self.cleaned_data["suppliers"])
            ingredient.recipes.set(self.cleaned_data["recipes"])
            ingredient.notifications.set(self.cleaned_data["notifications"])

        return save_m2m


class InventoryForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.order_by("name"),
        widget=forms.CheckboxSelectMultiple,
    )
    notifications = forms.ModelMultipleChoiceField(
        queryset=Notification.objects.order_by("-date", "-id"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Inventory
        fields = [
            "cafeteria",
            "ingredients",
            "notifications",
            "quantity_available",
            "expiration_date",
            "location",
        ]
        widgets = {
            "expiration_date": forms.DateInput(attrs={"type": "date"}),
        }

    def save(self, commit=True):
        inventory = super().save(commit=commit)
        if commit:
            inventory.ingredients.set(self.cleaned_data["ingredients"])
            inventory.notifications.set(self.cleaned_data["notifications"])
        else:
            self.save_m2m = self._save_m2m_for_unsaved_inventory(inventory)
        return inventory

    def _save_m2m_for_unsaved_inventory(self, inventory):
        def save_m2m():
            inventory.ingredients.set(self.cleaned_data["ingredients"])
            inventory.notifications.set(self.cleaned_data["notifications"])

        return save_m2m
