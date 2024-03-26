from django_filters import rest_framework as filters
from django.contrib.auth.models import Permission


class PermissionFilter(filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'content_type': ['exact'],
            'content_type__app_label': ['exact'],
            'content_type__model': ['exact'],
        }
