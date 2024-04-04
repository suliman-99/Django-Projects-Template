from django_filters import rest_framework as filters
from common.filters import FilterLookupExpr
from translation.methods import translate
from notification.models import Notification


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = {
            'user': FilterLookupExpr.OTHER,
            'is_viewed': FilterLookupExpr.BOOLEAN,
            **translate('title', FilterLookupExpr.STRING),
            **translate('body', FilterLookupExpr.STRING),
        }
