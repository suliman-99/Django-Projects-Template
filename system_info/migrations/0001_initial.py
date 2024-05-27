# Generated by Django 5.0.6 on 2024-05-27 20:24

import common.singleton_model.models
import django.db.models.deletion
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemInfo',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('privacy_policy', models.TextField()),
                ('privacy_policy_en', models.TextField(null=True)),
                ('privacy_policy_ar', models.TextField(null=True)),
                ('term_of_us', models.TextField()),
                ('term_of_us_en', models.TextField(null=True)),
                ('term_of_us_ar', models.TextField(null=True)),
                ('about_us', models.TextField()),
                ('about_us_en', models.TextField(null=True)),
                ('about_us_ar', models.TextField(null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(common.singleton_model.models.SingletonModel, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSystemInfo',
            fields=[
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('privacy_policy', models.TextField()),
                ('privacy_policy_en', models.TextField(null=True)),
                ('privacy_policy_ar', models.TextField(null=True)),
                ('term_of_us', models.TextField()),
                ('term_of_us_en', models.TextField(null=True)),
                ('term_of_us_ar', models.TextField(null=True)),
                ('about_us', models.TextField()),
                ('about_us_en', models.TextField(null=True)),
                ('about_us_ar', models.TextField(null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical system info',
                'verbose_name_plural': 'historical system infos',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
