from django.contrib import admin
from logger.models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'type',
        'user',
        'status_code',
        'url',
        'query_params',
        'request_headers',
        'request_body',
        'response_headers',
        'response_body',
        'created_at',
    )
    list_filter = (
        'type',
        'user',
        'status_code',
        'url',
        'created_at',
    )
    search_fields = (
        'user',
        'url',
        'query_params',
        'request_headers',
        'request_body',
        'response_headers',
        'response_body',
    )
