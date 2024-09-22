from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet
from common.rest_framework.permissions import ModelPermissions, IsAdmin, IsSuperuser
from ..serializers.group.main import (
    GetFullGroupSerializer,
    UpdateFullGroupSerializer,
)


class GroupViewSet(ModelViewSet):
    permission_models = Group
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    queryset = Group.objects.all() \
        .prefetch_related('permissions__content_type') \
        .prefetch_related('user_set')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetFullGroupSerializer
        return UpdateFullGroupSerializer
