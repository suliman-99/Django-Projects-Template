from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from translation.methods import full_translate
from .models import Notification, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(AuditModelAdmin):
    list_display = (
        'id',

        'user',
        'role',

        *full_translate('title'),
        *full_translate('body'),
        *full_translate('image'),

        'object_type',
        'object_id',

        'extra_data',

        'is_viewed',

        *audit_fields,
    )
    list_filter = (
        'role',
        'object_type',
        'is_viewed',

        *audit_fields,
    )
    search_fields = (
        'id',

        'user__id',
        'user__email',
        'user__phone_number',

        *full_translate('title'),
        *full_translate('body'),

        'object_id',
        
        'extra_data',
    )
    ordering = (
        '-updated_at',
    )


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(AuditModelAdmin):
    list_display = (
        'id',
        
        'type',

        *full_translate('title'),
        *full_translate('body'),
        *full_translate('image'),

        'extra_data',

        *audit_fields,
    )
    list_filter = (
        'type',

        *audit_fields,
    )
    search_fields = (
        'id',

        *full_translate('title'),
        *full_translate('body'),
        
        'extra_data',
    )
    ordering = (
        '-updated_at',
    )
