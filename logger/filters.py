from django_filters import rest_framework as filters
from logger.models import Log


class LogFilter(filters.FilterSet):
    class Meta:
        model = Log
        fields = {
            'created_at': ['lt', 'lte', 'gt', 'gte'],
            'level': ['exact'],
            'type': ['exact'],
            'user': ['exact'],
            'method': ['exact'],
            'url': ['exact', 'contains', 'icontains'],
            'message': ['exact'],
        }
