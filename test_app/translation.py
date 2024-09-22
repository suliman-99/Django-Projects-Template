from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models import Test


@register(Test)
class TestDeleteModelTranslationOptions(TranslationOptions):
    fields = (
        'text',
    )

simple_history.register(Test)
