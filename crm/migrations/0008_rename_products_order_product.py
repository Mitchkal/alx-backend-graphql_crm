# Generated by Django 5.2.3 on 2025-06-28 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_rename_product_order_products'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='products',
            new_name='product',
        ),
    ]
