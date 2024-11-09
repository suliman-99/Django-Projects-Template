from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from .models import Item


@admin.register(Item)
class ItemAdmin(AuditModelAdmin):
    pass
