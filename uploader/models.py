from django.db import models
from django.contrib.auth import get_user_model
from common.audit.models import HistoricalAuditModel


User = get_user_model()


class Item(HistoricalAuditModel):
    file = models.FileField(max_length=500, upload_to='uploads/')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='uploader_items')
