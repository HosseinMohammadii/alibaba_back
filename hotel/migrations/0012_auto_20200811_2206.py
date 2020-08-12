# Generated by Django 2.2.15 on 2020-08-11 22:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0011_hotel_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='stars',
            field=models.SmallIntegerField(blank=True, default=3, null=True, validators=[django.core.validators.MaxValueValidator(5)]),
        ),
    ]