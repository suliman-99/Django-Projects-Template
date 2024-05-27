from django.urls import path
from system_info.views import SystemInfoView


urlpatterns = [
    path('system-info/', SystemInfoView.as_view(), name='system-info'),
]
