from django_filters import rest_framework as filters
from logger.models import Log


class LogFilter(filters.FilterSet):
    class Meta:
        model = Log
        fields = {
            'type': ['exact'],
            'user': ['exact'],
            'status_code': ['exact', 'lt', 'lte', 'gt', 'gte'],
            'url': ['exact', 'contains', 'icontains'],
            'created_at': ['lt', 'lte', 'gt', 'gte'],
        }
