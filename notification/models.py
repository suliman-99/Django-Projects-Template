from django.db import models
from django.contrib.auth import get_user_model
from common.audit.models import AuditModel
from enums.enums import Role, NotificationObjectType, NotificationTemplateType


User = get_user_model()


class Notification(AuditModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    role = models.IntegerField(choices=Role.choices)

    title = models.TextField()
    body = models.TextField()
    image = models.ImageField(max_length=500, upload_to='notifications/images/', null=True, blank=True)

    object_type = models.PositiveIntegerField(choices=NotificationObjectType.choices, null=True, blank=True)
    object_id = models.CharField(max_length=50, null=True, blank=True)

    extra_data = models.JSONField(null=True, blank=True)

    is_viewed = models.BooleanField(default=False)


class NotificationTemplate(AuditModel):
    type = models.PositiveIntegerField(choices=NotificationTemplateType.choices, unique=True)

    title = models.TextField()
    body = models.TextField()
    image = models.ImageField(max_length=500, upload_to='notification_templates/images/', null=True, blank=True)

    extra_data = models.JSONField(null=True, blank=True)
