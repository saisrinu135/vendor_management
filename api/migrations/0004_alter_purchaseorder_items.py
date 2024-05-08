# Generated by Django 5.0.4 on 2024-05-06 17:07

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_purchaseorder_id_remove_vendor_vendor_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='items',
            field=models.JSONField(encoder=api.models.DecimalEncoder),
        ),
    ]