# Generated by Django 5.0.3 on 2024-04-04 07:25

import django.db.models.deletion
import notification.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalnotification',
            name='body_ar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicalnotification',
            name='body_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicalnotification',
            name='image_ar',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='historicalnotification',
            name='image_en',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='historicalnotification',
            name='title_ar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='historicalnotification',
            name='title_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='body_ar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='body_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='image_ar',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=notification.models.notification_image_path),
        ),
        migrations.AddField(
            model_name='notification',
            name='image_en',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to=notification.models.notification_image_path),
        ),
        migrations.AddField(
            model_name='notification',
            name='title_ar',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='title_en',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalnotification',
            name='body',
            field=models.TextField(default='body'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='historicalnotification',
            name='title',
            field=models.TextField(default='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='body',
            field=models.TextField(default='body'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='title',
            field=models.TextField(default='title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
