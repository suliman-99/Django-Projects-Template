from django_filters import rest_framework as filters
from common.rest_framework.filters import FilterLookupExpr
from logger.models import Log


class LogFilter(filters.FilterSet):
    class Meta:
        model = Log
        fields = {
            'created_at': FilterLookupExpr.DATETIME,
            'level': FilterLookupExpr.STRING,
            'type': FilterLookupExpr.STRING,
            'user': FilterLookupExpr.OTHER,
            'method': FilterLookupExpr.STRING,
            'url': FilterLookupExpr.STRING,
            'message': FilterLookupExpr.STRING,
        }
