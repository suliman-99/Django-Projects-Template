from django.contrib import admin
from fcm_django.models import FCMDevice
from fcm_django.admin import DeviceAdmin
from common.audit.admin import AuditModelAdmin
from .models import CustomFCMDevice


admin.site.unregister(FCMDevice)


@admin.register(CustomFCMDevice)
class CustomFCMDeviceAdmin(DeviceAdmin):
    pass
