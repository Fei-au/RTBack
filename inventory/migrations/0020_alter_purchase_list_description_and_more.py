# Generated by Django 5.0.1 on 2024-03-10 21:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0019_item_url_purchase_list"),
    ]

    operations = [
        migrations.AlterField(
            model_name="purchase_list",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="purchase_list",
            name="title",
            field=models.TextField(blank=True, null=True),
        ),
    ]
