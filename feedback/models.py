from django.db import models
from django.contrib.auth import get_user_model
from common.audit.models import HistoricalAuditModel


User = get_user_model()


class Feedback(HistoricalAuditModel):
    title = models.CharField(max_length=50)
    body = models.TextField()
