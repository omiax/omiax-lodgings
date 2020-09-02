# Generated by Django 2.2 on 2020-07-04 13:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_user_occupant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country_code',
            field=models.CharField(default='+234', max_length=4, validators=[django.core.validators.RegexValidator('^\\+\\d{1,3}[- ]?\\d{1,5}$')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=14, unique=True, validators=[django.core.validators.RegexValidator('^(\\+\\d{1,3}[- ]?|[0])?\\d{10}$')]),
        ),
    ]
