import django.core.validators
import django.utils.timezone
from django.db import migrations, models
import django.db.models.deletion
import supply.models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0002_align_models_with_assigned_erd_scope'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='delivery_details',
            new_name='delivery_frequency',
        ),
        migrations.AddField(
            model_name='supplier',
            name='rating',
            field=models.PositiveSmallIntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(5),
                ],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='supplier',
            name='delivery_frequency',
            field=models.CharField(
                choices=[
                    ('daily', 'Daily'),
                    ('weekly', 'Weekly'),
                    ('biweekly', 'Biweekly'),
                    ('monthly', 'Monthly'),
                    ('on_demand', 'On demand'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='expiry_date',
            field=models.DateField(
                default=django.utils.timezone.now,
                validators=[supply.models.validate_not_past],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ingredient',
            name='notification_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='recipe_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='reorder_threshold',
            new_name='threshold',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='storage_area',
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='quantity_unit',
            field=models.CharField(
                choices=[
                    ('kg', 'Kilogram'),
                    ('g', 'Gram'),
                    ('l', 'Liter'),
                    ('ml', 'Milliliter'),
                    ('pc', 'Piece'),
                    ('pack', 'Pack'),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='threshold',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='expiry_date',
            new_name='expiration_date',
        ),
        migrations.AddField(
            model_name='inventory',
            name='cafeteria_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='notification_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='expiration_date',
            field=models.DateField(validators=[supply.models.validate_future_date]),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='ingredient',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='inventory_records',
                to='supply.ingredient',
            ),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='quantity_available',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
