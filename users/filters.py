from django.contrib.auth.models import Permission
from django_filters import rest_framework as filters
from common.rest_framework.filters import FilterLookupExpr
from .models import User


class PermissionFilter(filters.FilterSet):
    class Meta:
        model = Permission
        fields = {
            'name': FilterLookupExpr.STRING,
            'content_type': FilterLookupExpr.OTHER,
            'content_type__app_label': FilterLookupExpr.OTHER,
            'content_type__model': FilterLookupExpr.OTHER,
        }


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'is_active': FilterLookupExpr.BOOLEAN,
            'is_admin': FilterLookupExpr.BOOLEAN,

            'date_joined': FilterLookupExpr.DATE,
            'first_login': FilterLookupExpr.DATETIME,
            'last_login': FilterLookupExpr.DATETIME,
            'last_refresh': FilterLookupExpr.DATETIME,

            'email': FilterLookupExpr.STRING,
            'email_verified': FilterLookupExpr.BOOLEAN,

            'phone_number': FilterLookupExpr.STRING,
            'phone_number_verified': FilterLookupExpr.BOOLEAN,

            'first_name': FilterLookupExpr.STRING,
            'last_name': FilterLookupExpr.STRING,
            'language_code': FilterLookupExpr.OTHER,
        }
