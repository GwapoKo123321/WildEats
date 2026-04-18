from django.db import models


class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=100)
    OrderDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.OrderID} - {self.CustomerName}"


class OrderItem(models.Model):
    OrderItemID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ProductName = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.ProductName} (x{self.Quantity})"


class PaymentRecord(models.Model):
    PaymentID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentMethod = models.CharField(max_length=50)
    PaymentDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.PaymentID} - {self.Amount}"


from django.db import models

# Create your models here.
