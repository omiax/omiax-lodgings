# Generated by Django 2.2 on 2020-12-31 13:01

from django.db import migrations, models
import payments.models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_payment_tenant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='manual_pay',
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_image',
            field=models.ImageField(blank=True, null=True, upload_to=payments.models.image_file_path),
        ),
    ]
