from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from common.singleton_model.admin import SingletonModelAdmin
from system_info.models import SystemInfo


@admin.register(SystemInfo)
class SystemInfoAdmin(SingletonModelAdmin, AuditModelAdmin):
    list_display = (
        'id',
        'privacy_policy',
        'term_of_us',
        'about_us',
        *audit_fields,
    )
    list_filter = (
        'id',
        *audit_fields,
    )
    search_fields = (
        'privacy_policy',
        'term_of_us',
        'about_us',
    )
    ordering = (
        '-id', 
    )
