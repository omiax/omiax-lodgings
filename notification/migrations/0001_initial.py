# Generated by Django 2.2 on 2021-01-16 15:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffNotificationList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator('^(\\+\\d{1,3}[- ]?|[0])?\\d{10}$')])),
                ('staff', models.ForeignKey(blank=True, limit_choices_to={'is_staff': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.CharField(max_length=255)),
                ('rating', models.CharField(choices=[('N', 'Normal'), ('D', 'Danger')], default='N', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
