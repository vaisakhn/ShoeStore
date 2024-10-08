# Generated by Django 5.0.6 on 2024-10-05 16:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordersummary',
            name='delivery_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=200),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
