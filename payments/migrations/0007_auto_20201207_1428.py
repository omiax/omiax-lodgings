# Generated by Django 2.2 on 2020-12-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0006_auto_20201207_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='app_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='merchant_fee',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_plan',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_ref',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
