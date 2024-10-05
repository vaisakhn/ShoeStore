# Generated by Django 5.0.6 on 2024-10-05 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_ordersummary_order_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordersummary',
            name='product_object',
        ),
        migrations.AddField(
            model_name='ordersummary',
            name='cart_items_object',
            field=models.ManyToManyField(to='store.cartitems'),
        ),
    ]
