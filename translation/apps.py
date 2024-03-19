from django.apps import AppConfig


class TranslationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'translation'

    def ready(self) -> None:
        import translation.signals.handlers
        return super().ready()
