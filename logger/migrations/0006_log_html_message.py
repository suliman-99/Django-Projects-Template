# Generated by Django 5.0.3 on 2024-03-24 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0005_remove_log_response_headers'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='html_message',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
