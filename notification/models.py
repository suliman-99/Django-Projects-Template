from django.db import models
from django.contrib.auth import get_user_model
from common.audit.models import HistoricalAuditModel


User = get_user_model()


def notification_image_path(notification, filename):
    return f'notifications/images/{filename}'


class Notification(HistoricalAuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_viewed = models.BooleanField(default=False)

    title = models.JSONField(null=True, blank=True)
    body = models.JSONField(null=True, blank=True)
    image = models.ImageField(max_length=500, upload_to=notification_image_path, null=True, blank=True)
