from rest_framework.generics import CreateAPIView, RetrieveAPIView
from common.rest_framework.permissions import IsAdmin
from .models import SystemInfo
from .serializers import AdminSystemInfoSerializer, SystemInfoSerializer


class AdminSystemInfoView(RetrieveAPIView, CreateAPIView):
    permission_classes = (IsAdmin, )
    serializer_class = AdminSystemInfoSerializer
    
    def get_object(self):
        return SystemInfo.objects.filter().first()


class SystemInfoView(RetrieveAPIView):
    serializer_class = SystemInfoSerializer
    
    def get_object(self):
        return SystemInfo.objects.filter().first()
