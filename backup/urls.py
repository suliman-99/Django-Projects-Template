from django.urls import path
from backup.views import Backup


urlpatterns = [
    path('backups/', Backup.as_view(), name='backups'),
]
