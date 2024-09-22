from uuid import uuid4
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
from safedelete.models import (
    SOFT_DELETE_CASCADE,
    SafeDeleteModel, 
    # SafeDeleteManager,
    # SafeDeleteAllManager,
    # SafeDeleteDeletedManager,
)
# from ..audit.querysets import SafeDeleteBulkSignalQuerySet


User = settings.AUTH_USER_MODEL



class AuditModel(SafeDeleteModel):
    '''
    Use `AuditModel` when you want to register HistoricalRecords after doing something with the concrete model
    Main example: Using django-modeltranslation in the model then using the django history 
    '''
    class Meta:
        abstract = True

    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    
    created_by = models.ForeignKey(User, models.DO_NOTHING, null=True, blank=True, related_name="+")
    updated_by = models.ForeignKey(User, models.DO_NOTHING, null=True, blank=True, related_name="+")

    # objects = SafeDeleteManager(SafeDeleteBulkSignalQuerySet)
    # all_objects = SafeDeleteAllManager(SafeDeleteBulkSignalQuerySet)
    # deleted_objects = SafeDeleteDeletedManager(SafeDeleteBulkSignalQuerySet)


class HistoricalAuditModel(AuditModel):
    '''
    Use `HistoricalAuditModel` when you want to register HistoricalRecords automatically right after initializing the class
    '''
    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)
