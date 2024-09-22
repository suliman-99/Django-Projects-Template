from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from .models import CustomFCMDevice
from .serializers import CustomFCMDeviceSerializer


class CustomFCMDeviceAuthorizedViewSet(FCMDeviceAuthorizedViewSet):
    queryset = CustomFCMDevice.objects.all()
    serializer_class = CustomFCMDeviceSerializer
