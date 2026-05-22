from django.db import migrations, models


OLD_PAYMENT_STATUS = "Re" + "jected"
OLD_ORDER_STATUS = "Payment " + OLD_PAYMENT_STATUS
NEW_PAYMENT_STATUS = "Failed"
NEW_ORDER_STATUS = "Payment Failed"


def rename_old_statuses(apps, schema_editor):
    Order = apps.get_model("salesandtransactions", "Order")
    PaymentRecord = apps.get_model("salesandtransactions", "PaymentRecord")

    Order.objects.filter(OrderStatus=OLD_ORDER_STATUS).update(OrderStatus=NEW_ORDER_STATUS)
    PaymentRecord.objects.filter(PaymentStatus=OLD_PAYMENT_STATUS).update(
        PaymentStatus=NEW_PAYMENT_STATUS
    )


def restore_old_statuses(apps, schema_editor):
    Order = apps.get_model("salesandtransactions", "Order")
    PaymentRecord = apps.get_model("salesandtransactions", "PaymentRecord")

    Order.objects.filter(OrderStatus=NEW_ORDER_STATUS).update(OrderStatus=OLD_ORDER_STATUS)
    PaymentRecord.objects.filter(PaymentStatus=NEW_PAYMENT_STATUS).update(
        PaymentStatus=OLD_PAYMENT_STATUS
    )


class Migration(migrations.Migration):

    dependencies = [
        ("salesandtransactions", "0006_paymentrecord_verifiedbyvendor_alter_menuitem_price_and_more"),
    ]

    operations = [
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
                    ("Cancelled", "Cancelled"),
                    ("Deleted", "Deleted"),
                ],
                default="Pending Payment",
                max_length=20,
            ),
        ),
        migrations.AlterField(
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
        migrations.RunPython(rename_old_statuses, restore_old_statuses),
    ]
