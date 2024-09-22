from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from translation.methods import full_translate
from .models import TestTimeModel, Test, SubTest


@admin.register(Test)
class TestAdmin(AuditModelAdmin):
    list_display = (
        'id',
        'bool',
        'num',
        'date',
        'time',
        'datetime',
        'duration',
        *full_translate('text'),
        'un',
        *audit_fields,
    )
    list_filter = (
        'bool',
        'num',
        'date',
        'time',
        'datetime',
        'duration',
        *full_translate('text'),
        'un',
        *audit_fields,
    )
    search_fields = (
        'id',
        'date',
        'time',
        'datetime',
        'duration',
        *full_translate('text'),
        'un',
    )
    ordering = (
        '-updated_at',
    )


@admin.register(SubTest)
class SubtestAdmin(AuditModelAdmin):
    list_display = (
        'id',
        'test', 
        'text',
        *audit_fields,
    )
    list_filter = (
        'test',
        *audit_fields,
    )
    search_fields = (
        'id',
        'test_id',
        'text',
    )
    ordering = (
        '-updated_at',
    )


@admin.register(TestTimeModel)
class TestTimeModelAdmin(AuditModelAdmin):
    list_display = (
        'id',
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
    list_filter = (
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
    search_fields = (
        'id',
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
    ordering = (
        '-created_at',
    )
