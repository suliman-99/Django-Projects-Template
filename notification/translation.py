from modeltranslation.translator import register, TranslationOptions
import simple_history
from notification.models import Notification


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'body',
        'image',
    )
simple_history.register(Notification)
