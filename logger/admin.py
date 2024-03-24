from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminTextareaWidget
from logger.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'level',
        'type',
        'user',
        'method',
        'url',
        'message',
        'query_params',
        'request_headers',
    )
    list_filter = (
        'created_at',
        'level',
        'type',
        'user',
        'method',
        'url',
        'message',
    )
    search_fields = (
        'user',
        'url',
        'message',
        'query_params',
        'request_headers',
    )
    ordering = (
        '-created_at', 
    )
    formfield_overrides = {
        models.JSONField: {'widget': AdminTextareaWidget },
    }
    # readonly_fields = (
    #     'view_html_messsage',
    # )

    # def view_html_messsage(self, obj):
    #     return mark_safe(obj.html_message)
