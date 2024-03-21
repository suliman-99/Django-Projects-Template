from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Log(models.Model):
    TYPE_API = 'api'
    TYPE_ADMIN = 'admin'
    TYPE_OTHERS = 'others'
    TYPE_CHOICES = (
        (TYPE_API, TYPE_API),
        (TYPE_ADMIN, TYPE_ADMIN),
        (TYPE_OTHERS, TYPE_OTHERS),
    )

    type = models.CharField(choices=TYPE_CHOICES, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='logs')
    status_code = models.PositiveIntegerField()
    method = models.CharField(max_length=10)
    url = models.TextField()
    query_params = models.JSONField()
    request_headers = models.JSONField()
    request_body = models.JSONField(null=True, blank=True)
    response_headers = models.JSONField()
    response_body = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
