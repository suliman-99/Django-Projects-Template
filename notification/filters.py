from django_filters import rest_framework as filters
from common.rest_framework.filters import FilterLookupExpr
from translation.methods import full_translate
from .models import Notification


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = {
            'id': FilterLookupExpr.OTHER,
            'user': FilterLookupExpr.OTHER,
            'is_viewed': FilterLookupExpr.BOOLEAN,
            **full_translate('title', FilterLookupExpr.STRING),
            **full_translate('body', FilterLookupExpr.STRING),
        }
