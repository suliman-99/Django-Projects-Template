from django.contrib.auth import get_user_model
from fcm_django.api.rest_framework import FCMDeviceSerializer
from .models import CustomFCMDevice


User = get_user_model()


class CustomFCMDeviceSerializer(FCMDeviceSerializer):
    class Meta:
        model = CustomFCMDevice
        fields = (
            "id",
            "name",
            "registration_id",
            "device_id",
            "active",
            "date_created",
            "type",
            "role",
        )
