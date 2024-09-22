from django.contrib import admin
from fcm_django.models import FCMDevice
from fcm_django.admin import DeviceAdmin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from .models import CustomFCMDevice


admin.site.unregister(FCMDevice)


@admin.register(CustomFCMDevice)
class CustomFCMDeviceAdmin(AuditModelAdmin, DeviceAdmin):
    list_display = (
        "id",
        "registration_id",
        "user",
        "device_id",
        "name",
        "type",
        "role",
        "active",
        *audit_fields,
    )
    list_filter = (
        "type",
        "role",
        "active",
        *audit_fields,
    )
    search_fields = (
        "id",
        "registration_id",
        "user__id",
        "user__email",
        "user__phone_number",
        "device_id",
        "name",
    )
    ordering = (
        '-updated_at',
    )
