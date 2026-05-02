from django.db import models
from django.core.exceptions import ValidationError


class Cafeteria(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class FoodItem(models.Model):
    Cafeteria = models.ForeignKey('Cafeteria', on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    PortionSize = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Cafeteria', 'Name'], name='unique_food_per_cafeteria')
        ]

    def __str__(self):
        return self.Name


class Ingredient(models.Model):
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Recipe(models.Model):
    RecipeID = models.AutoField(primary_key=True)
    FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    PreparationTime = models.IntegerField()
    Instructions = models.TextField()

    Ingredients = models.ManyToManyField(Ingredient)

    def clean(self):
        if self.PreparationTime <= 0:
            raise ValidationError("Preparation time must be greater than zero.")

        if not self.Instructions.strip():
            raise ValidationError("Instructions cannot be empty.")

    def __str__(self):
        return f"Recipe for {self.FoodItem.Name}"


class NutritionInfo(models.Model):
    NutritionInfoID = models.AutoField(primary_key=True)
    FoodItem = models.OneToOneField(FoodItem, on_delete=models.CASCADE)
    Calories = models.FloatField()
    Protein = models.FloatField()
    Fat = models.FloatField()
    Carbs = models.FloatField()
    Sodium = models.FloatField()

    def clean(self):
        values = [self.Calories, self.Protein, self.Fat, self.Carbs, self.Sodium]
        if any(v < 0 for v in values):
            raise ValidationError("Nutritional values must be zero or positive.")

    def __str__(self):
        return f"Nutrition for {self.FoodItem.Name}"