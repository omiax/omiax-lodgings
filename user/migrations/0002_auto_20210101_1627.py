# Generated by Django 2.2 on 2021-01-01 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='account_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
