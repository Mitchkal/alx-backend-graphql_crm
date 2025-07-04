# Generated by Django 5.2.3 on 2025-06-27 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_product_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_id',
        ),
        migrations.AddField(
            model_name='order',
            name='product_id',
            field=models.ManyToManyField(related_name='orders', to='crm.product'),
        ),
    ]
