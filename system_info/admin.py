from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.singleton_model.admin import SingletonModelAdmin
from .models import SystemInfo


@admin.register(SystemInfo)
class SystemInfoAdmin(SingletonModelAdmin, AuditModelAdmin):
    pass
