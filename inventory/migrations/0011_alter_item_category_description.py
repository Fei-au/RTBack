# Generated by Django 5.0.1 on 2024-02-09 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_item_add_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item_category',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
