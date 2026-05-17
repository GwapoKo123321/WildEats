# # from django.db import models
# # from django.core.exceptions import ValidationError
# #
# #
# # class Cafeteria(models.Model):
# #     Name = models.CharField(max_length=100)
# #
# #     def __str__(self):
# #         return self.Name
# #
# #
# # class FoodItem(models.Model):
# #     Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
# #     Name = models.CharField(max_length=100)
# #     Price = models.DecimalField(max_digits=10, decimal_places=2)
# #     PortionSize = models.CharField(max_length=50)
# #
# #     class Meta:
# #         constraints = [
# #             models.UniqueConstraint(fields=['Cafeteria', 'Name'], name='unique_food_per_cafeteria')
# #         ]
# #
# #     def __str__(self):
# #         return self.Name
# #
# #
# # class Ingredient(models.Model):
# #     Name = models.CharField(max_length=100, unique=True)
# #
# #     def __str__(self):
# #         return self.Name
# #
# #
# # class Recipe(models.Model):
# #     RecipeID = models.AutoField(primary_key=True)
# #     FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
# #     PreparationTime = models.IntegerField()
# #     Instructions = models.TextField()
# #     Ingredients = models.ManyToManyField(Ingredient, blank=True)
# #
# #     def clean(self):
# #         if self.PreparationTime <= 0:
# #             raise ValidationError("Preparation time must be greater than zero.")
# #         if not self.Instructions.strip():
# #             raise ValidationError("Instructions cannot be empty.")
# #
# #     def __str__(self):
# #         return f"Recipe for {self.FoodItem.Name}"
# #
# #
# # class NutritionInfo(models.Model):
# #     NutritionInfoID = models.AutoField(primary_key=True)
# #     FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
# #     Calories = models.FloatField()
# #     Protein = models.FloatField()
# #     Fat = models.FloatField()
# #     Carbs = models.FloatField()
# #     Sodium = models.FloatField()
# #
# #     def clean(self):
# #         values = [self.Calories, self.Protein, self.Fat, self.Carbs, self.Sodium]
# #         if any(v < 0 for v in values):
# #             raise ValidationError("Nutritional values must be zero or positive.")
# #
# #     def __str__(self):
# #         return f"Nutrition for {self.FoodItem.Name}"
#
# from django.db import models
# from django.core.exceptions import ValidationError
#
#
# class Cafeteria(models.Model):
#     Name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.Name
#
#
# class FoodItem(models.Model):
#     Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
#     Name = models.CharField(max_length=100)
#     Price = models.DecimalField(max_digits=10, decimal_places=2)
#     PortionSize = models.CharField(max_length=50)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields=['Cafeteria', 'Name'], name='unique_food_per_cafeteria')
#         ]
#
#     def __str__(self):
#         return self.Name
#
#
# class Ingredient(models.Model):
#     Name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.Name
#
#
# class Recipe(models.Model):
#     RecipeID = models.AutoField(primary_key=True)
#     FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
#     PreparationTime = models.IntegerField()
#     Instructions = models.TextField()
#     Ingredients = models.ManyToManyField(Ingredient, blank=True)
#
#     def clean(self):
#         if self.PreparationTime <= 0:
#             raise ValidationError("Preparation time must be greater than zero.")
#         if not self.Instructions.strip():
#             raise ValidationError("Instructions cannot be empty.")
#
#     def __str__(self):
#         return f"Recipe for {self.FoodItem.Name}"
#
#
# class NutritionInfo(models.Model):
#     NutritionInfoID = models.AutoField(primary_key=True)
#     FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
#     Calories = models.FloatField()
#     Protein = models.FloatField()
#     Fat = models.FloatField()
#     Carbs = models.FloatField()
#     Sodium = models.FloatField()
#
#     def clean(self):
#         values = [self.Calories, self.Protein, self.Fat, self.Carbs, self.Sodium]
#         if any(v < 0 for v in values):
#             raise ValidationError("Nutritional values must be zero or positive.")
#
#     def __str__(self):
#         return f"Nutrition for {self.FoodItem.Name}"

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


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


# class Ingredient(models.Model):
#     Name = models.CharField(max_length=100, unique=True)
#     IsAllergen = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.Name

class Ingredient(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    IsAllergen = models.BooleanField(default=False)

    def __str__(self):
        return self.Name


class FoodItem(models.Model):
    Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
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