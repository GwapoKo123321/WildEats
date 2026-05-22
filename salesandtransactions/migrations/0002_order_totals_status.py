from decimal import Decimal

from django.db import migrations, models


def populate_order_totals(apps, schema_editor):
    Order = apps.get_model("salesandtransactions", "Order")

    for order in Order.objects.all():
        total_cost = sum(
            (item.Quantity * item.Price for item in order.items.all()),
            Decimal("0.00"),
        )
        total_paid = sum(
            (payment.Amount for payment in order.payments.all()),
            Decimal("0.00"),
        )

        if total_paid == Decimal("0.00"):
            status = "Unpaid"
        elif total_paid < total_cost:
            status = "Partially Paid"
        else:
            status = "Paid"

        order.TotalCost = total_cost
        order.TotalPaid = total_paid
        order.OrderStatus = status
        order.save(update_fields=["TotalCost", "TotalPaid", "OrderStatus"])


class Migration(migrations.Migration):

    dependencies = [
        ("salesandtransactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="OrderStatus",
            field=models.CharField(
                choices=[
                    ("Unpaid", "Unpaid"),
                    ("Partially Paid", "Partially Paid"),
                    ("Paid", "Paid"),
                ],
                default="Unpaid",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="TotalCost",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0.00"),
                max_digits=10,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="TotalPaid",
            field=models.DecimalField(
                decimal_places=2,
                default=Decimal("0.00"),
                max_digits=10,
            ),
        ),
        migrations.RunPython(populate_order_totals, migrations.RunPython.noop),
    ]
