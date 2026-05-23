from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


def validate_not_past(value):
    if value < timezone.localdate():
        raise ValidationError("Date must not be earlier than the current date.")


def validate_future_date(value):
    if value <= timezone.localdate():
        raise ValidationError("Date must be later than the current date.")


class Supplier(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"

    DELIVERY_FREQUENCY_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (BIWEEKLY, "Biweekly"),
        (MONTHLY, "Monthly"),
        (ON_DEMAND, "On demand"),
    ]

    ingredient_id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    contact_info = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    delivery_frequency = models.CharField(
        max_length=20,
        choices=DELIVERY_FREQUENCY_CHOICES,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    KILOGRAM = "kg"
    GRAM = "g"
    LITER = "l"
    MILLILITER = "ml"
    PIECE = "pc"
    PACK = "pack"

    QUANTITY_UNIT_CHOICES = [
        (KILOGRAM, "Kilogram"),
        (GRAM, "Gram"),
        (LITER, "Liter"),
        (MILLILITER, "Milliliter"),
        (PIECE, "Piece"),
        (PACK, "Pack"),
    ]

    recipe_id = models.PositiveIntegerField(null=True, blank=True)
    inventory_id = models.PositiveIntegerField(null=True, blank=True)
    notification_id = models.PositiveIntegerField(null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    quantity_unit = models.CharField(max_length=10, choices=QUANTITY_UNIT_CHOICES)
    threshold = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    storage_condition = models.CharField(max_length=100)
    expiry_date = models.DateField(validators=[validate_not_past])
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name


class Inventory(models.Model):
    cafeteria_id = models.PositiveIntegerField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='inventory_records')
    notification_id = models.PositiveIntegerField(null=True, blank=True)
    quantity_available = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    expiration_date = models.DateField(validators=[validate_future_date])
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity_available}"
