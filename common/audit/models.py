from uuid import uuid4
from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from simple_history.models import HistoricalRecords


class AuditModel(SafeDeleteModel):
    class Meta:
        abstract = True

    _safedelete_policy = SOFT_DELETE_CASCADE

    history = HistoricalRecords(inherit=True)

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)