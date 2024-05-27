from rest_framework.generics import CreateAPIView, RetrieveAPIView
from common.rest_framework.permissions import IsAdminOrReadOnly
from system_info.models import SystemInfo
from system_info.serializers import SystemInfoSerializer


class SystemInfoView(CreateAPIView, RetrieveAPIView):
    permission_classes = (IsAdminOrReadOnly, )
    serializer_class = SystemInfoSerializer
    
    def get_object(self):
        return SystemInfo.objects.filter().first()
