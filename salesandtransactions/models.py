from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class MenuItem(models.Model):
    MenuItemID = models.AutoField(primary_key=True)
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="menu_items",
        db_column="Vendor_id",
    )
    name = models.CharField(max_length=100, db_column="Name")
    description = models.TextField(blank=True, db_column="Description")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        db_column="Price",
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    is_available = models.BooleanField(default=True, db_column="IsAvailable")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CreatedAt")
    updated_at = models.DateTimeField(auto_now=True, db_column="UpdatedAt")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - \u20b1{self.price:.2f}"


class Order(models.Model):
    STATUS_PENDING_PAYMENT = "Pending Payment"
    STATUS_PAYMENT_SUBMITTED = "Payment Submitted"
    STATUS_PAYMENT_VERIFIED = "Payment Verified"
    STATUS_PAYMENT_FAILED = "Payment Failed"
    STATUS_PROCESSING = "Processing"
    STATUS_COMPLETED = "Completed"
    STATUS_CANCELLED = "Cancelled"
    STATUS_DELETED = "Deleted"
    STATUS_CHOICES = [
        (STATUS_PENDING_PAYMENT, STATUS_PENDING_PAYMENT),
        (STATUS_PAYMENT_SUBMITTED, STATUS_PAYMENT_SUBMITTED),
        (STATUS_PAYMENT_VERIFIED, STATUS_PAYMENT_VERIFIED),
        (STATUS_PAYMENT_FAILED, STATUS_PAYMENT_FAILED),
        (STATUS_PROCESSING, STATUS_PROCESSING),
        (STATUS_COMPLETED, STATUS_COMPLETED),
        (STATUS_CANCELLED, STATUS_CANCELLED),
        (STATUS_DELETED, STATUS_DELETED),
    ]

    OrderID = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=100)
    OrderDate = models.DateTimeField(auto_now_add=True)
    TotalCost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    TotalPaid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
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
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

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

    @property
    def is_inactive(self):
        return self.is_deleted or self.OrderStatus in {
            self.STATUS_CANCELLED,
            self.STATUS_DELETED,
        }

    @property
    def can_cancel(self):
        if self.pk is None:
            return True
        return not self.is_inactive and not self.payments.exists()

    def cancel(self, save=True):
        if not self.can_cancel:
            raise ValidationError("Orders linked to payment records cannot be cancelled.")
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.OrderStatus = self.STATUS_CANCELLED
        if save:
            self.save(update_fields=["is_deleted", "deleted_at", "OrderStatus"])

    def delete(self, *args, **kwargs):
        if self.payments.exists():
            raise ValidationError("Orders linked to payment records cannot be deleted.")
        return super().delete(*args, **kwargs)

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
    MenuItem = models.ForeignKey(
        MenuItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="Item_id",
    )
    ProductName = models.CharField(max_length=100)
    Quantity = models.PositiveIntegerField()
    Price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    Subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )

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
    STATUS_FAILED = "Failed"
    STATUS_CHOICES = [
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_VERIFIED, STATUS_VERIFIED),
        (STATUS_FAILED, STATUS_FAILED),
    ]

    PaymentID = models.AutoField(primary_key=True)
    Order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    Amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    PaymentMethod = models.CharField(max_length=50)
    PaymentDate = models.DateTimeField(auto_now_add=True)
    CashPayment = models.BooleanField(default=True)
    VerifiedByVendor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="verified_payments",
        null=True,
        blank=True,
    )
    PaymentStatus = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    def __str__(self):
        return f"Payment {self.PaymentID} - {self.Amount}"
