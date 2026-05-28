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


class Cafeteria(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=100)
    operating_hours = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Notification(models.Model):
    date = models.DateField(default=timezone.localdate)
    view_status = models.BooleanField(default=False)

    def __str__(self):
        status = "Viewed" if self.view_status else "Unread"
        return f"{status} notification on {self.date}"


class Recipe(models.Model):
    preparation_time = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    instructions = models.TextField()
    ingredients = models.ManyToManyField(
        "Ingredient",
        through="RecipeIngredient",
        related_name="recipes",
    )

    def __str__(self):
        return f"Recipe {self.pk}"


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_info = models.CharField(max_length=255)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    delivery_frequency = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)
    quantity_unit = models.CharField(max_length=50)
    threshold = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    storage_condition = models.CharField(max_length=100)
    expiry_date = models.DateField(validators=[validate_not_past])
    notifications = models.ManyToManyField(
        Notification,
        through="IngredientNotification",
        related_name="ingredients",
        blank=True,
    )
    suppliers = models.ManyToManyField(
        Supplier,
        through="IngredientSupplier",
        related_name="ingredients",
    )

    def __str__(self):
        return self.name


class Inventory(models.Model):
    cafeteria = models.ForeignKey(
        Cafeteria,
        on_delete=models.CASCADE,
        related_name="inventory_records",
        null=True,
        blank=True,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientInventory",
        related_name="inventory_records",
    )
    notifications = models.ManyToManyField(
        Notification,
        through="InventoryNotification",
        related_name="inventory_records",
        blank=True,
    )
    quantity_available = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    expiration_date = models.DateField(validators=[validate_future_date])
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.quantity_available} available at {self.location}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        db_table = "supply_recipe_uses_ingredient"
        constraints = [
            models.UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            )
        ]

    def __str__(self):
        return f"{self.recipe} uses {self.ingredient}"


class IngredientSupplier(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = "supply_ingredient_supplied_by"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "supplier"],
                name="unique_ingredient_supplier",
            )
        ]

    def __str__(self):
        return f"{self.ingredient} supplied by {self.supplier}"


class IngredientInventory(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)

    class Meta:
        db_table = "supply_ingredient_stored_in_inventory"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "inventory"],
                name="unique_ingredient_inventory",
            )
        ]

    def __str__(self):
        return f"{self.ingredient} stored in {self.inventory}"


class IngredientNotification(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = "supply_ingredient_generates_notification"
        constraints = [
            models.UniqueConstraint(
                fields=["ingredient", "notification"],
                name="unique_ingredient_notification",
            )
        ]

    def __str__(self):
        return f"{self.ingredient} generated {self.notification}"


class InventoryNotification(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)

    class Meta:
        db_table = "supply_inventory_generates_notification"
        constraints = [
            models.UniqueConstraint(
                fields=["inventory", "notification"],
                name="unique_inventory_notification",
            )
        ]

    def __str__(self):
        return f"{self.inventory} generated {self.notification}"
