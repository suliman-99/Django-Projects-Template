from django.urls import path
from logger.views import LogListAPIView


urlpatterns = [
    path('logs/', LogListAPIView.as_view(), name='logs'),
]
