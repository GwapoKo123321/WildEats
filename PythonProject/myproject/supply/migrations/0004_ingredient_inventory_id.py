from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0003_enforce_supply_business_rules'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='inventory_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
