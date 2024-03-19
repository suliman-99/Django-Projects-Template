from django.db import models
from django.db.models.signals import post_save


class CustomManager(models.Manager):
    """
    send signals when `bulk_create()` or `bulk_update()` is called
    """
    def bulk_update(self, *args, **kwargs):
        ret = super().bulk_update(*args, **kwargs)
        post_save.send(sender=self.model)
        return ret
    
    def bulk_create(self, *args, **kwargs):
        ret = super().bulk_create(*args, **kwargs)
        post_save.send(sender=self.model)
        return ret
