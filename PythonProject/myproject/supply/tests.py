from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from .models import Ingredient, Inventory, Supplier


class SupplyBusinessRuleTests(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Green Valley Farms",
            contact_info="green@example.com",
            rating=5,
            delivery_frequency="Weekly",
        )

    def test_supplier_name_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(
                name="Green Valley Farms",
                contact_info="other@example.com",
                rating=4,
                delivery_frequency="Daily",
            )

    def test_supplier_rating_must_be_between_one_and_five(self):
        supplier = Supplier(
            name="Low Rated Supplier",
            contact_info="low@example.com",
            rating=6,
            delivery_frequency="Monthly",
        )

        with self.assertRaises(ValidationError):
            supplier.full_clean()

    def test_ingredient_uses_unit_and_current_or_future_expiry(self):
        ingredient = Ingredient(
            name="Tomato",
            quantity_unit="kg",
            threshold=10,
            storage_condition="Cold storage",
            expiry_date=timezone.localdate(),
        )

        ingredient.full_clean()
        ingredient.save()
        ingredient.suppliers.add(self.supplier)
        self.assertEqual(list(ingredient.suppliers.all()), [self.supplier])

    def test_ingredient_expiry_cannot_be_in_the_past(self):
        ingredient = Ingredient(
            name="Expired Lettuce",
            quantity_unit="pc",
            threshold=5,
            storage_condition="Chilled",
            expiry_date=timezone.localdate() - timedelta(days=1),
        )

        with self.assertRaises(ValidationError):
            ingredient.full_clean()

    def test_inventory_accepts_nonnegative_quantity_and_future_expiration(self):
        ingredient = Ingredient.objects.create(
            name="Rice",
            quantity_unit="kg",
            threshold=20,
            storage_condition="Dry storage",
            expiry_date=timezone.localdate() + timedelta(days=30),
        )
        ingredient.suppliers.add(self.supplier)
        inventory = Inventory(
            quantity_available=0,
            expiration_date=timezone.localdate() + timedelta(days=1),
            location="Main Pantry",
        )

        inventory.full_clean()
        inventory.save()
        inventory.ingredients.add(ingredient)
        self.assertEqual(list(inventory.ingredients.all()), [ingredient])

    def test_inventory_rejects_negative_quantity_and_current_expiration(self):
        ingredient = Ingredient.objects.create(
            name="Flour",
            quantity_unit="kg",
            threshold=15,
            storage_condition="Dry storage",
            expiry_date=timezone.localdate() + timedelta(days=30),
        )
        ingredient.suppliers.add(self.supplier)
        inventory = Inventory(
            quantity_available=-1,
            expiration_date=timezone.localdate(),
            location="Main Pantry",
        )

        with self.assertRaises(ValidationError):
            inventory.full_clean()
