# Generated by Django 5.0.3 on 2024-03-25 13:07

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_first_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
    ]
