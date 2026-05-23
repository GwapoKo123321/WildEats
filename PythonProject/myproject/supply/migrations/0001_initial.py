import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('contact_info', models.CharField(max_length=255)),
                ('rating', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0)])),
                ('delivery_time', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('quantity_unit', models.CharField(max_length=50)),
                ('threshold', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('storage_condition', models.CharField(max_length=100)),
                ('expiry_date', models.DateField()),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='supply.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_available', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('expiration_date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('ingredient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='supply.ingredient')),
            ],
        ),
    ]
