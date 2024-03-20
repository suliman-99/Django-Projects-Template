# Generated by Django 5.0.3 on 2024-03-20 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('api', 'api'), ('admin', 'admin'), ('others', 'others')], max_length=10)),
                ('status_code', models.PositiveIntegerField()),
                ('url', models.TextField()),
                ('query_params', models.JSONField()),
                ('request_headers', models.JSONField()),
                ('request_body', models.JSONField()),
                ('response_headers', models.JSONField()),
                ('response_body', models.JSONField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
