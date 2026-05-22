from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_order_statuses(apps, schema_editor):
    Order = apps.get_model("salesandtransactions", "Order")
    status_map = {
        "Unpaid": "Pending Payment",
        "Partially Paid": "Payment Submitted",
        "Paid": "Payment Verified",
    }

    for order in Order.objects.all():
        order.OrderStatus = status_map.get(order.OrderStatus, order.OrderStatus)
        order.save(update_fields=["OrderStatus"])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("salesandtransactions", "0002_order_totals_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="Student",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="student_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="Vendor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="vendor_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="paymentrecord",
            name="CashPayment",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="paymentrecord",
            name="PaymentStatus",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Verified", "Verified"),
                    ("Failed", "Failed"),
                ],
                default="Pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="OrderStatus",
            field=models.CharField(
                choices=[
                    ("Pending Payment", "Pending Payment"),
                    ("Payment Submitted", "Payment Submitted"),
                    ("Payment Verified", "Payment Verified"),
                    ("Payment Failed", "Payment Failed"),
                    ("Processing", "Processing"),
                    ("Completed", "Completed"),
                ],
                default="Pending Payment",
                max_length=20,
            ),
        ),
        migrations.RunPython(migrate_order_statuses, migrations.RunPython.noop),
    ]
