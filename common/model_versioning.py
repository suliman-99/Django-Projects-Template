from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models


def model_versioning_signal_handler(origin_model, version_model):
    @receiver(post_save, sender=origin_model, weak=False)
    def model_versioning(**kwargs):
        instance = kwargs['instance']

        last_version = version_model.objects.filter(origin=instance).aggregate(last_version=models.Max('version')).get('last_version', 0)
        last_version = last_version if last_version else 0

        new_version_instance = version_model()
        new_version_instance.origin = instance
        new_version_instance.version = last_version + 1

        for field in instance._meta.fields:
            if field.name not in ('id', 'pk'):
                setattr(new_version_instance, field.name, getattr(instance, field.name))

        new_version_instance.save()
