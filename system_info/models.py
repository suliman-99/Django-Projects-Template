from django.db import models
from safedelete.models import (
    SafeDeleteManager,
    SafeDeleteAllManager,
    SafeDeleteDeletedManager,
)
from common.audit.models import AuditModel
from common.singleton_model.models import SingletonModel
from common.singleton_model.querysets import SingletonQuerySet


class SystemInfo(SingletonModel, AuditModel):
    privacy_policy = models.TextField()
    term_of_us = models.TextField()
    about_us = models.TextField()

    objects = SafeDeleteManager(SingletonQuerySet)
    all_objects = SafeDeleteAllManager(SingletonQuerySet)
    deleted_objects = SafeDeleteDeletedManager(SingletonQuerySet)
