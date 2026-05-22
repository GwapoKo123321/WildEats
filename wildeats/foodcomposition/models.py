from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
import datetime


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('vendor', 'Vendor'),
        ('student', 'Student'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    Fname = models.CharField(max_length=100, blank=True)
    Lname = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class AdminProfile(models.Model):
    CAFETERIA_CHOICES = [('college', 'College'), ('highschool', 'High School')]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    AdminLevel = models.CharField(max_length=50)
    CafeteriaType = models.CharField(max_length=20, choices=CAFETERIA_CHOICES)

    def __str__(self):
        return f"Admin: {self.user.username}"


class VendorProfile(models.Model):
    CONTRACT_CHOICES = [('active', 'Active'), ('pending', 'Pending'), ('expired', 'Expired')]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    ContactNumber = models.CharField(max_length=20)
    BusinessLicenseNumber = models.CharField(max_length=100, unique=True)
    ContractStatus = models.CharField(max_length=20, choices=CONTRACT_CHOICES, default='pending')

    def __str__(self):
        return f"Vendor: {self.user.username}"


class Cafeteria(models.Model):
    Name = models.CharField(max_length=100)
    Location = models.CharField(max_length=200, default='')
    OperatingHours = models.CharField(max_length=100, default='', help_text="e.g. 7:00 AM - 5:00 PM")
    Capacity = models.IntegerField(default=1)

    def clean(self):
        if self.Capacity <= 0:
            raise ValidationError("Capacity must be greater than zero.")

    def __str__(self):
        return self.Name


CATEGORY_CHOICES = [
    ('breakfast', 'Breakfast'),
    ('lunch', 'Lunch'),
    ('dinner', 'Dinner'),
    ('snack', 'Snack'),
    ('drinks', 'Drinks'),
]

COMMON_INGREDIENTS = [
    ('milk', 'Milk'),
    ('eggs', 'Eggs'),
    ('wheat', 'Wheat'),
    ('soy', 'Soy'),
    ('peanuts', 'Peanuts'),
    ('tree_nuts', 'Tree Nuts'),
    ('fish', 'Fish'),
    ('shellfish', 'Shellfish'),
    ('garlic', 'Garlic'),
    ('onion', 'Onion'),
    ('chicken', 'Chicken'),
    ('beef', 'Beef'),
    ('pork', 'Pork'),
    ('rice', 'Rice'),
    ('flour', 'Flour'),
    ('sugar', 'Sugar'),
    ('salt', 'Salt'),
    ('butter', 'Butter'),
    ('oil', 'Oil'),
    ('tomato', 'Tomato'),
]

class Ingredient(models.Model):
    UNIT_CHOICES = [
        ('g', 'Grams (g)'),
        ('kg', 'Kilograms (kg)'),
        ('ml', 'Milliliters (ml)'),
        ('L', 'Liters (L)'),
        ('pcs', 'Pieces (pcs)'),
        ('tbsp', 'Tablespoon (tbsp)'),
        ('tsp', 'Teaspoon (tsp)'),
        ('cup', 'Cup'),
    ]
    Name = models.CharField(max_length=100, unique=True)
    QuantityUnit = models.CharField(max_length=20, choices=UNIT_CHOICES, default='g')
    Threshold = models.FloatField(default=0, help_text="Minimum stock before alert")
    StorageCondition = models.CharField(max_length=200, default='')
    ExpiryDate = models.DateField(null=True, blank=True)
    IsAllergen = models.BooleanField(default=False)

    def clean(self):
        if self.Threshold < 0:
            raise ValidationError("Threshold must be zero or positive.")

    def __str__(self):
        return self.Name

# class FoodItem(models.Model):
#     Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
#     Name = models.CharField(max_length=100)
#     Price = models.DecimalField(max_digits=10, decimal_places=2)
#     PortionSize = models.CharField(max_length=50)
#     Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lunch')
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['Cafeteria', 'Name'], name='unique_food_per_cafeteria')
#         ]
#
#     def clean(self):
#         if self.Price is not None and self.Price <= 0:
#             raise ValidationError("Price must be greater than zero.")
#
#     def __str__(self):
#         return self.Name

class FoodItem(models.Model):
    Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
    Discount = models.ForeignKey('Discount', on_delete=models.SET_NULL, null=True, blank=True)
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    PortionSize = models.CharField(max_length=50)
    Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lunch')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Cafeteria', 'Name'], name='unique_food_per_cafeteria')
        ]

    def clean(self):
        if self.Price is not None and self.Price <= 0:
            raise ValidationError("Price must be greater than zero.")

    def discounted_price(self):
        if self.Discount and self.Discount.is_active():
            discount_amount = float(self.Price) * (self.Discount.Percentage / 100)
            return round(float(self.Price) - discount_amount, 2)
        return None

    def __str__(self):
        return self.Name


class Recipe(models.Model):
    FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    PreparationTime = models.IntegerField()
    Instructions = models.TextField()
    Ingredients = models.ManyToManyField(Ingredient, blank=True)

    def clean(self):
        if self.PreparationTime is not None and self.PreparationTime <= 0:
            raise ValidationError("Preparation time must be greater than zero.")
        if self.Instructions and not self.Instructions.strip():
            raise ValidationError("Instructions cannot be empty.")

    def __str__(self):
        return f"Recipe for {self.FoodItem.Name}"


class NutritionInfo(models.Model):
    FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    Calories = models.FloatField(help_text="kcal")
    Protein = models.FloatField(help_text="g")
    Fat = models.FloatField(help_text="g")
    Carbs = models.FloatField(help_text="g")
    Sodium = models.FloatField(help_text="mg")

    def clean(self):
        values = [self.Calories, self.Protein, self.Fat, self.Carbs, self.Sodium]
        if any(v is not None and v < 0 for v in values):
            raise ValidationError("Nutritional values must be zero or positive.")

    def __str__(self):
        return f"Nutrition for {self.FoodItem.Name}"


class Discount(models.Model):
    Name = models.CharField(max_length=100)
    Description = models.TextField(blank=True)
    StartDate = models.DateField()
    EndDate = models.DateField()
    Percentage = models.FloatField(help_text="Percentage between 1 and 100")

    def clean(self):
        if self.Percentage < 1 or self.Percentage > 100:
            raise ValidationError("Discount percentage must be between 1 and 100.")
        if self.StartDate and self.EndDate and self.StartDate >= self.EndDate:
            raise ValidationError("Start date must be before end date.")

    def is_active(self):
        today = datetime.date.today()
        return self.StartDate <= today <= self.EndDate

    def __str__(self):
        return f"{self.Name} ({self.Percentage}%)"