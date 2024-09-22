import sys
from django.apps import AppConfig


class SchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'scheduler'

    def ready(self) -> None:
        if not 'makemigrations' in sys.argv and not 'migrate' in sys.argv:
            from . import schedular
            schedular.start()
