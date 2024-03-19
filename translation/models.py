from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from common.audit.models import AuditModel
from translation.managers import CustomManager


class Language(AuditModel):
    """
    Table store all languages
    """
    name = models.CharField(max_length=50, unique=True)
    native_name = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        try:
            old_instance = self.__class__.objects.get(pk=self.pk) 
        except:
            old_instance = None
            
        ret = super().save(*args, **kwargs)

        # here the save is applied successfully and we have to send the signal
        if old_instance:
            post_save.send(sender=self.__class__, old_instance=old_instance, new_instance=self)

        return ret

    def __str__(self) -> str:
        return f'{self.name} - {self.code}'


class Translation(AuditModel):
    """
    Table store all translations values
    """
    content_type =  models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=50)
    field_name =  models.CharField(max_length=50)
    language_code = models.CharField(max_length=10)
    value = models.TextField()

    objects = CustomManager()

    def __str__(self) -> str:
        return f'{self.content_type} - {self.object_id} - {self.field_name} - {self.language_code} - {self.value}'
