# Generated by Django 5.0.1 on 2024-03-18 19:27

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("inventory", "0022_auction_product_list"),
    ]

    operations = [
        migrations.RenameField(
            model_name="auction_product_list",
            old_name="lot_number",
            new_name="image_number",
        ),
    ]
