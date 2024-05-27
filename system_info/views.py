from rest_framework.generics import CreateAPIView, RetrieveAPIView
from common.rest_framework.permissions import IsAdmin
from system_info.models import SystemInfo
from system_info.serializers import AdminSystemInfoSerializer, SystemInfoSerializer


class AdminSystemInfoView(RetrieveAPIView, CreateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = AdminSystemInfoSerializer
    
    def get_object(self):
        return SystemInfo.objects.filter().first()


class SystemInfoView(RetrieveAPIView):
    serializer_class = SystemInfoSerializer
    
    def get_object(self):
        return SystemInfo.objects.filter().first()
