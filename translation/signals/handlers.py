from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from translation.models import Language
from translation.cache import load_languages


@receiver(post_delete, sender=Language, weak=False)
@receiver(post_save, sender=Language, weak=False)
def reload_languages(**kwargs):
    load_languages()
