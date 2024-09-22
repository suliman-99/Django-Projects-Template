from modeltranslation.translator import register, TranslationOptions
import simple_history
from .models import Notification, NotificationTemplate


@register(Notification)
class NotificationTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'body',
        'image',
    )
simple_history.register(Notification)


@register(NotificationTemplate)
class NotificationTemplateTranslationOptions(TranslationOptions):
    fields = (
        'title', 
        'body',
        'image',
    )
simple_history.register(NotificationTemplate)
