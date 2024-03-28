from rest_framework.filters import BaseFilterBackend
from django.db.models.query_utils import Q


class AllFieldsFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter = Q()
        
        for key in request.query_params.keys():
            values = request.query_params.getlist(key)
            if key in [field.name for field in view.queryset.model._meta.fields]:
                filter &= Q( **{ key + '__in': values })
        
        return queryset.filter(filter)


class FilterLookupExpr:
    EXACT = 'exact'
    CONTAINS = 'contains'
    ICONTAINS = 'icontains'
    LT = 'lt'
    LTE = 'lte'
    GT = 'gt'
    GTE = 'gte'

    BOOLEAN = (EXACT, )
    NUMBER = (EXACT, LT, LTE, GT, GTE)
    STRING = (EXACT, CONTAINS, ICONTAINS)
    DATE= (EXACT, LT, LTE, GT, GTE)
    TIME = (EXACT, LT, LTE, GT, GTE)
    DATETIME = (EXACT, LT, LTE, GT, GTE)
    DURATION = (EXACT, LT, LTE, GT, GTE)
    OTHER = (EXACT,)
