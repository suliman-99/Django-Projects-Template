from rest_framework.viewsets import ModelViewSet
from common.rest_framework.permissions import ModelPermissions, IsAdmin, IsSuperuser
from users.models import User
from users.filters import UserFilter
from users.serializers.user.main import (
    GetFullUserSerializer,
    UpdateFullUserSerializer,
)


class UserViewSet(ModelViewSet):
    permission_models = User
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    filterset_class = UserFilter
    queryset = User.objects.all() \
        .prefetch_related('user_permissions__content_type') \
        .prefetch_related('groups')
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetFullUserSerializer
        return UpdateFullUserSerializer
