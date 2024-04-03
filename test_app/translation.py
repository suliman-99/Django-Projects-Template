from modeltranslation.translator import register, TranslationOptions
import simple_history
from test_app.models import Test


@register(Test)
class TestDeleteModelTranslationOptions(TranslationOptions):
    fields = (
        'text',
        'new_text',
    )

simple_history.register(Test)
