from django_filters import rest_framework as filters


class EnumModelFilter(filters.FilterSet):
    name__icontains = filters.CharFilter(field_name='name', lookup_expr='icontains')
