from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminTextareaWidget
from logger.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'user',
        'status_code',
        'method',
        'url',
        'created_at',
        'query_params',
        'request_headers',
        # 'request_body',
        'response_headers',
        # 'response_body',
    )
    list_filter = (
        'type',
        'user',
        'status_code',
        'method',
        'url',
        'created_at',
    )
    search_fields = (
        'user',
        'method',
        'url',
        'query_params',
        'request_headers',
        'request_body',
        'response_headers',
        'response_body',
    )
    formfield_overrides = {
        models.JSONField: {'widget': AdminTextareaWidget },
    }
