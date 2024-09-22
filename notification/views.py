from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from common.rest_framework.permissions import ModelPermissions, IsAdmin, IsSuperuser
from common.rest_framework.pagination import CustomLimitOffsetPagination
from .models import Notification
from .filters import NotificationFilter
from .serializers import (
    SendNotificationSerializer,
    GetNotificationSerializer,
    FullNotificationSerializer,
)


class NotificationViewSet(viewsets.ModelViewSet):
    permission_models = Notification
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    queryset = Notification.objects.all()
    filterset_class = NotificationFilter
    search_fields = (
        'title',
        'body',
    )
    ordering_fields = (
        'is_viewed',
        'created_at',
        'updated_at',
    )
    
    def get_serializer_class(self):
        if self.action == 'send_notifications':
            return SendNotificationSerializer
        return FullNotificationSerializer
    
    @action(detail=False, methods=['post'], url_path='send-notifications')
    def send_notifications(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class MyNotificationViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    permission_classes = (permissions.IsAuthenticated, )
    filterset_class = NotificationFilter
    pagination_class = CustomLimitOffsetPagination
    search_fields = (
        'title',
        'body',
    )
    ordering_fields = (
        'is_viewed',
        'created_at',
        'updated_at',
    )
    serializer_class_action_map = {
        'retrieve': GetNotificationSerializer,
        'list': GetNotificationSerializer,
    }

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return self.serializer_class_action_map[self.action]
    
    @action(detail=True, methods=['put'], url_path='mark-as-viewed')
    def mark_as_viewed(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_viewed = True
        instance.save()
        return Response({})
    
    @action(detail=False, methods=['put'], url_path='mark-all-as-viewed')
    def mark_all_as_viewed(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset.filter(is_viewed=False).update(is_viewed=True)
        return Response({})
