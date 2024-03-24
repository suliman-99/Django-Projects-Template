from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Log(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='logs')
    method = models.CharField(max_length=10)
    url = models.TextField()
    message = models.TextField()
    html_message = models.TextField()
    query_params = models.JSONField()
    request_headers = models.JSONField()
