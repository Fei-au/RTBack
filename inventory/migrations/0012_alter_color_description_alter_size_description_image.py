# Generated by Django 5.0.1 on 2024-02-12 17:51

import django.db.models.deletion
import inventory.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_alter_item_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='size',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('local_image', models.ImageField(blank=True, null=True, upload_to=inventory.models.upload_to)),
                ('external_url', models.URLField(blank=True, max_length=255, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='inventory.item')),
            ],
        ),
    ]