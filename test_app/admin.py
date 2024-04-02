from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from test_app.models import TestTranslationModel, TestTimeModel, TestDeleteModel, TestDeleteModel2


@admin.register(TestTranslationModel)
class TestTranslationModelAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'translated_text',
    )


@admin.register(TestTimeModel)
class TestTimeModelAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )


@admin.register(TestDeleteModel)
class TestDeleteModelAdmin(AuditModelAdmin):
    list_display = (
        'text',
        'un',
        *audit_fields,
    )


@admin.register(TestDeleteModel2)
class TestDeleteModel2Admin(AuditModelAdmin):
    list_display = (
        'base', 
        'text',
        *audit_fields,
    )
