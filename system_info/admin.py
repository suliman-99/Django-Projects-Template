from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from common.singleton_model.admin import SingletonModelAdmin
from translation.methods import full_translate
from .models import SystemInfo


@admin.register(SystemInfo)
class SystemInfoAdmin(SingletonModelAdmin, AuditModelAdmin):
    list_display = (
        'id',
        *full_translate('privacy_policy'),
        *full_translate('term_of_us'),
        *full_translate('about_us'),
        *audit_fields,
    )
    list_editable = (
        *full_translate('privacy_policy'),
        *full_translate('term_of_us'),
        *full_translate('about_us'),
    )
