from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0004_ingredient_inventory_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='ingredient_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
