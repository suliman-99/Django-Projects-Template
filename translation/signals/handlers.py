from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from translation.models import Translation, Language
from translation.functions import load_translations, load_languages


@receiver(post_delete, sender=Translation, weak=False)
@receiver(post_save, sender=Translation, weak=False)
def reload_translations(**kwargs):
    """ Method to reload the cached data whenever the `Translation` table is changed """
    load_translations()


@receiver(post_delete, sender=Language, weak=False)
@receiver(post_save, sender=Language, weak=False)
def reload_languages(**kwargs):
    """ 
    Method to reload the cached data whenever the `Language` table is changed 

    Note: `Language.code` field is a ForeignKey referenced in the `Translation.language_code` field
    so, after loading the new data the method will check about the changes on the `Language.code` field
    then apply these changes on the `Translation.language_code` field
    """
    load_languages()
    old_instance = kwargs.get('old_instance')
    new_instance = kwargs.get('new_instance')
    if not old_instance or not new_instance or old_instance.code == new_instance.code:
        return
    update_objs = []
    for translation in Translation.objects.all():
        if translation.language_code == old_instance.code:
            translation.language_code = new_instance.code
            update_objs.append(translation)
    Translation.objects.bulk_update(update_objs, ['language_code'])
