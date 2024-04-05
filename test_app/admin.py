from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from translation.methods import full_translate
from test_app.models import TestTimeModel, Test, SubTest


@admin.register(Test)
class TestAdmin(AuditModelAdmin):
    list_display = (
        'id',
        *full_translate('text'),
        'un',
        *audit_fields,
    )
    list_filter = (
        *full_translate('text'),
        'un',
        *audit_fields,
    )
    search_fields = (
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
        'text',
        *audit_fields,
    )
    search_fields = (
        'text',
    )
    ordering = (
        '-updated_at',
    )


@admin.register(TestTimeModel)
class TestTimeModelAdmin(admin.ModelAdmin):
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
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
    ordering = (
        '-created_at',
    )
