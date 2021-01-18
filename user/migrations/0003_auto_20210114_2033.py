# Generated by Django 2.2 on 2021-01-14 19:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210101_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='account_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bank_account_name',
        ),
        migrations.CreateModel(
            name='UserBankInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_name', models.CharField(blank=True, max_length=255, null=True)),
                ('account_number', models.CharField(blank=True, max_length=255, null=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
