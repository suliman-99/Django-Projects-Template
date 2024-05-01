from django_filters import rest_framework as filters
from django.contrib.auth.models import Permission
from common.rest_framework.filters import FilterLookupExpr


class PermissionFilter(filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'content_type': FilterLookupExpr.OTHER,
            'content_type__app_label': FilterLookupExpr.STRING,
            'content_type__model': FilterLookupExpr.STRING,
        }
