# Generated by Django 5.0.4 on 2024-04-22 10:23

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='historicaluser',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('email',), name='unique_active_email'),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('phone_number',), name='unique_active_phone_number'),
        ),
    ]
