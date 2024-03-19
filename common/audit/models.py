from uuid import uuid4
from django.db import models
from django.conf import settings


UserModel = settings.AUTH_USER_MODEL


class NotDeletedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_deleted=False)


class AuditModel(models.Model):
    class Meta:
        abstract = True

    objects = models.Manager()
    not_deleted_objects = NotDeletedManager()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    created_by = models.ForeignKey(UserModel, models.DO_NOTHING, null=True, blank=True, related_name="+")
    
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
    updated_by = models.ForeignKey(UserModel, models.DO_NOTHING, null=True, blank=True, related_name="+")
    
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(UserModel, models.DO_NOTHING, null=True, blank=True, related_name="+")
    is_deleted = models.BooleanField(default=False)
