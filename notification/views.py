from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from rest_framework.response import Response
from common.permissions import IsSuperuser
from notification.models import Notification
from notification.filters import NotificationFilter
from notification.serializers import (
    SendNotificationSerializer, 
    GetNotificationSerializer, 
    MarkNotificationAsViewedSerializer,
    FullNotificationSerializer,
)


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSuperuser, )
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
        if self.request.method == 'POST':
            return SendNotificationSerializer
        return FullNotificationSerializer


class MyNotificationViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'put']
    permission_classes = (permissions.IsAuthenticated, )
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
    serializer_class_action_map = {
        'retrieve': GetNotificationSerializer,
        'list': GetNotificationSerializer,
        'mark_as_viewed': MarkNotificationAsViewedSerializer,
    }

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        return self.serializer_class_action_map[self.action]
    
    @action(detail=True, methods=['put'])
    def mark_as_viewed(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    @action(detail=False, methods=['put'])
    def mark_all_as_viewed(self, request, *args, **kwargs):
        self.get_queryset().filter(is_viewed=False).update(is_viewed=True)
        return Response({})
