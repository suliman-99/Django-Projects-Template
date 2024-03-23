from django.db import models
from common.audit.models import AuditModel


class Language(AuditModel):
    name = models.CharField(max_length=50, unique=True)
    native_name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name} - {self.code}'
