# Generated by Django 5.0.3 on 2024-03-21 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0002_alter_log_request_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='method',
            field=models.CharField(default='un-known', max_length=10),
            preserve_default=False,
        ),
    ]