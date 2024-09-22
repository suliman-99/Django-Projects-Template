from rest_framework.generics import ListAPIView
from common.rest_framework.permissions import IsSuperuser
from .models import Log
from .serializers import LogSerializer
from .filters import LogFilter


class LogListAPIView(ListAPIView):
    permission_classes = (IsSuperuser, )
    queryset = Log.objects.all()
    filterset_class = LogFilter
    serializer_class = LogSerializer
