from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone

class Cafeteria(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    operating_hours = models.CharField(max_length=50)
    capacity = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name

class Report(models.Model):
    REPORT_TYPES = [
        ('Inventory', 'Inventory'),
        ('Sales', 'Sales'),
        ('Nutrition', 'Nutrition'),
    ]
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    date_generated = models.DateTimeField(default=timezone.now)
    report_summary = models.TextField()

    def __str__(self):
        return f"{self.report_type} - {self.date_generated.strftime('%Y-%m-%d')}"

class Notification(models.Model):
    STATUS_CHOICES = [('Read', 'Read'), ('Unread', 'Unread')]
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True)
    ingredient_id = models.IntegerField(null=True, blank=True)
    order_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unread')

    def __str__(self):
        return f"Alert {self.id}: {self.status}"