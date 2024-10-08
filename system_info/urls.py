from django.urls import path
from .views import AdminSystemInfoView, SystemInfoView


urlpatterns = [
    path('admin-system-info/', AdminSystemInfoView.as_view(), name='admin-system-info'),
    path('system-info/', SystemInfoView.as_view(), name='system-info'),
]
