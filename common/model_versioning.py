from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models


def model_versioning_signal_handler(origin_model, version_model):
    @receiver(post_save, sender=origin_model, weak=False)
    def model_versioning(**kwargs):
        instance = kwargs['instance']
        instance_id = instance.id
        last_version = version_model.objects.filter(origin_id=instance_id).aggregate(last_version=models.Max('version')).get('last_version', 0)
        last_version = last_version if last_version else 0
        instance.__class__ = version_model
        instance.id = None
        instance.origin_id = instance_id
        instance.version = last_version + 1
        instance.save()
