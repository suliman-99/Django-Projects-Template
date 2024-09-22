from django.urls import path
from .views import Backup


urlpatterns = [
    path('backups/', Backup.as_view(), name='backups'),
]
