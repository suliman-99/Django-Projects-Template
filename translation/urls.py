from django.urls import path
from .views import LanguageListAPIView


urlpatterns = [
    path('languages/', LanguageListAPIView.as_view(), name='languages'),
]
