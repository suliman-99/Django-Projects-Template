from rest_framework.generics import ListAPIView
from common.permissions import IsSuperuser
from logger.models import Log
from logger.serializers import LogSerializer
from logger.filters import LogFilter


class LogListAPIView(ListAPIView):
    permission_classes = (IsSuperuser, )
    queryset = Log.objects.all()
    filterset_class = LogFilter
    serializer_class = LogSerializer
