from django.contrib.auth.models import Permission
from rest_framework.viewsets import ModelViewSet
from common.rest_framework.permissions import ModelPermissions, IsAdmin, IsSuperuser
from ..filters import PermissionFilter
from ..serializers.permission import PermissionSerializer


class PermissionViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_models = Permission
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    serializer_class = PermissionSerializer
    queryset = Permission.objects.prefetch_related('content_type')
    filterset_class = PermissionFilter
    search_fields = (
        'name',
    )
