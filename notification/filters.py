from django_filters import rest_framework as filters
from notification.models import Notification


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = {
            'user': ['exact'],
            'is_viewed': ['exact'],
            'title': ['contains'],
            'body': ['contains'],
        }
