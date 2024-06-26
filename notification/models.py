from django.db import models
from django.contrib.auth import get_user_model
from common.audit.models import AuditModel


User = get_user_model()


def notification_image_path(notification, filename):
    return f'notifications/images/{filename}'


class Notification(AuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_viewed = models.BooleanField(default=False)

    title = models.TextField()
    body = models.TextField()
    image = models.ImageField(max_length=500, upload_to=notification_image_path, null=True, blank=True)
