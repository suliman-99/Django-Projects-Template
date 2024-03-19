from django.db import models
from common.audit.models import AuditModel


class TestTimeModel(AuditModel):
    created_at = models.DateTimeField(auto_now_add=True)
    timezone_now = models.DateTimeField()
    timezone_localtime_timezone_now = models.DateTimeField()
