# Generated by Django 5.0.1 on 2024-02-08 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_alter_supplier_added_date'),
        ('staff', '0003_rename_staff_profile_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='add_staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='staff.profile'),
        ),
    ]
