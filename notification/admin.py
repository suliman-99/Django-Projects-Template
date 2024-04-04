from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from translation.methods import full_translate
from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(AuditModelAdmin):
    list_display = (
        'id',

        *full_translate('title'),
        *full_translate('body'),
        *full_translate('image'),

        'user',
        'is_viewed',

        *audit_fields,
    )
