from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from translation.methods import translate
from test_app.models import TestTimeModel, Test, SubTest


@admin.register(Test)
class TestAdmin(AuditModelAdmin):
    list_display = (
        'text',
        *translate('text'),
        'un',
        *audit_fields,
    )


@admin.register(SubTest)
class SubtestAdmin(AuditModelAdmin):
    list_display = (
        'test', 
        'text',
        *audit_fields,
    )


@admin.register(TestTimeModel)
class TestTimeModelAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
