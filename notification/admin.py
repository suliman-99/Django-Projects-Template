from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from .models import Notification, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(AuditModelAdmin):
    pass


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(AuditModelAdmin):
    pass
