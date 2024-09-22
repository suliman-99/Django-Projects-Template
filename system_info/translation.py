from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models import SystemInfo


@register(SystemInfo)
class SystemInfoTranslationOptions(TranslationOptions):
    fields = (
        'privacy_policy',
        'term_of_us',
        'about_us',
    )
simple_history.register(SystemInfo)
