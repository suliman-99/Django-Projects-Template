# Generated by Django 5.0.6 on 2024-09-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fcm', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfcmdevice',
            name='role',
            field=models.IntegerField(choices=[(1, 'Superuser'), (2, 'Admin')]),
        ),
        migrations.AlterField(
            model_name='historicalcustomfcmdevice',
            name='role',
            field=models.IntegerField(choices=[(1, 'Superuser'), (2, 'Admin')]),
        ),
    ]
