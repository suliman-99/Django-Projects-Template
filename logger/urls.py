from django.urls import path
from .views import LogListAPIView


urlpatterns = [
    path('logs/', LogListAPIView.as_view(), name='logs'),
]
