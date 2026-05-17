from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    STATUS_PENDING_PAYMENT = "Pending Payment"
    STATUS_PAYMENT_SUBMITTED = "Payment Submitted"
    STATUS_PAYMENT_VERIFIED = "Payment Verified"
    STATUS_PAYMENT_REJECTED = "Payment Rejected"
    STATUS_PROCESSING = "Processing"
    STATUS_COMPLETED = "Completed"
    STATUS_CHOICES = [
        (STATUS_PENDING_PAYMENT, STATUS_PENDING_PAYMENT),
        (STATUS_PAYMENT_SUBMITTED, STATUS_PAYMENT_SUBMITTED),
        (STATUS_PAYMENT_VERIFIED, STATUS_PAYMENT_VERIFIED),
        (STATUS_PAYMENT_REJECTED, STATUS_PAYMENT_REJECTED),
        (STATUS_PROCESSING, STATUS_PROCESSING),
        (STATUS_COMPLETED, STATUS_COMPLETED),
    ]

    OrderID = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=100)
    OrderDate = models.DateTimeField(auto_now_add=True)
    TotalCost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    TotalPaid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    OrderStatus = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING_PAYMENT,
    )
    Student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_orders",
        null=True,
        blank=True,
    )
    Vendor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="vendor_orders",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Order {self.OrderID} - {self.CustomerName}"

    @property
    def total_amount(self):
        return self.TotalCost

    @property
    def paid_amount(self):
        return self.TotalPaid

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount

    def recompute_totals(self, save=True):
        if hasattr(self, "_prefetched_objects_cache"):
            self._prefetched_objects_cache.pop("items", None)
            self._prefetched_objects_cache.pop("payments", None)

        self.TotalCost = sum((item.line_total for item in self.items.all()), Decimal("0.00"))
        self.TotalPaid = sum(
            (
                payment.Amount
                for payment in self.payments.filter(PaymentStatus=PaymentRecord.STATUS_VERIFIED)
            ),
            Decimal("0.00"),
        )

        if save:
            self.save(update_fields=["TotalCost", "TotalPaid"])


class OrderItem(models.Model):
    OrderItemID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ProductName = models.CharField(max_length=100)
    Quantity = models.IntegerField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def __str__(self):
        return f"{self.ProductName} (x{self.Quantity})"

    @property
    def line_total(self):
        return self.Subtotal or self.Quantity * self.Price

    def save(self, *args, **kwargs):
        self.Subtotal = self.Quantity * self.Price
        super().save(*args, **kwargs)


class PaymentRecord(models.Model):
    STATUS_PENDING = "Pending"
    STATUS_VERIFIED = "Verified"
    STATUS_REJECTED = "Rejected"
    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_VERIFIED, STATUS_VERIFIED),
        (STATUS_REJECTED, STATUS_REJECTED),
    ]

    PaymentID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    Amount = models.DecimalField(max_digits=10, decimal_places=2)
    PaymentMethod = models.CharField(max_length=50)
    PaymentDate = models.DateTimeField(auto_now_add=True)
    CashPayment = models.BooleanField(default=True)
    PaymentStatus = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    def __str__(self):
        return f"Payment {self.PaymentID} - {self.Amount}"
