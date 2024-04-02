from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(AuditModelAdmin):
    list_display = (
        'id',

        'title',
        'body',
        'image',

        'user',
        'is_viewed',

        *audit_fields,
    )
