from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supply', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='delivery_time',
            new_name='delivery_details',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='rating',
        ),
        migrations.RenameField(
            model_name='ingredient',
            old_name='threshold',
            new_name='reorder_threshold',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='expiry_date',
        ),
        migrations.AddField(
            model_name='ingredient',
            name='storage_area',
            field=models.CharField(default='General Storage', max_length=100),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='inventory',
            old_name='expiration_date',
            new_name='expiry_date',
        ),
    ]
