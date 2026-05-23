from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone



class Cafeteria(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    operating_hours = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class Menu(models.Model):
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=100)
    description = models.TextField()


class MealPlan(models.Model):
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE, related_name='meal_plans')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Inventory(models.Model):
    cafeteria = models.ForeignKey(Cafeteria, on_delete=models.CASCADE, related_name='inventory')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Ready', 'Ready')]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)


class Report(models.Model):
    REPORT_TYPES = [('Inventory', 'Inventory'), ('Sales', 'Sales'), ('Nutrition', 'Nutrition')]
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date_generated = models.DateTimeField(default=timezone.now)
    report_summary = models.TextField()

    def clean(self):

        if self.date_generated > timezone.now():
            raise ValidationError('Date cannot be in the future.')

        if not self.report_summary or not self.report_summary.strip():
            raise ValidationError('Report summaries cannot be empty.')


class Notification(models.Model):
    STATUS_CHOICES = [('Read', 'Read'), ('Unread', 'Unread')]


    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, null=True, blank=True)

    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unread')