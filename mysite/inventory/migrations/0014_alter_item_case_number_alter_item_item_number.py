# Generated by Django 5.0.1 on 2024-02-13 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0013_alter_image_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='case_number',
            field=models.CharField(default=1, max_length=12),
        ),
        migrations.AlterField(
            model_name='item',
            name='item_number',
            field=models.CharField(blank=True, default=1, max_length=20, null=True),
        ),
    ]
