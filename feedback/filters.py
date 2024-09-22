from django_filters import rest_framework as filters
from common.rest_framework.filters import FilterLookupExpr
from .models import Feedback


class FeedbackFilter(filters.FilterSet):
    class Meta:
        model = Feedback
        fields = {
            'title': FilterLookupExpr.STRING,
            'body': FilterLookupExpr.STRING,
        }
