# Generated by Django 4.2.3 on 2023-10-03 14:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system_management', '0004_type_remove_otp_enter_attempts_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempts',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
