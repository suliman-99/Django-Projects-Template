from django_filters import rest_framework as filters
from common.filters import FilterLookupExpr
from translation.methods import full_translate
from test_app.models import Test, SubTest


class UpdateTestFilter(filters.FilterSet):
    class Meta:
        model = Test
        fields = {
            **full_translate('text', FilterLookupExpr.STRING),
            'un': FilterLookupExpr.NUMBER,
        }


class GetTestFilter(filters.FilterSet):
    class Meta:
        model = Test
        fields = {
            'text': FilterLookupExpr.STRING,
            'un': FilterLookupExpr.NUMBER,
        }


class SubTestFilter(filters.FilterSet):
    class Meta:
        model = SubTest
        fields = {
            'test': FilterLookupExpr.OTHER,
            'text': FilterLookupExpr.STRING,
        }
