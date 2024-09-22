from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from .models import Item


@admin.register(Item)
class ItemAdmin(AuditModelAdmin):
    list_display = (
        'id',
        'file',
        'user',
        *audit_fields,
    )
    list_filter = (
        'user',
        *audit_fields,
    )
    search_fields = (
        'id',
        'file',
        'user__id',
        'user__email',
        'user__phone_number',
    )
    ordering = (
        '-updated_at',
    )
