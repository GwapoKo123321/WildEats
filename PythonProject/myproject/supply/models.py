from django.core.validators import MinValueValidator
from django.db import models


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_info = models.CharField(max_length=255)
    delivery_details = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity_unit = models.CharField(max_length=50)
    reorder_threshold = models.IntegerField(validators=[MinValueValidator(0)])
    storage_condition = models.CharField(max_length=100)
    storage_area = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='ingredients')

    def __str__(self):
        return self.name


class Inventory(models.Model):
    ingredient = models.OneToOneField(Ingredient, on_delete=models.CASCADE, related_name='inventory')
    quantity_available = models.IntegerField(validators=[MinValueValidator(0)])
    expiry_date = models.DateField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ingredient.name} - {self.quantity_available}"
