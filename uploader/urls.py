from django.urls import path
from .views import ItemCreateAPIView


urlpatterns = [
    path('items/', ItemCreateAPIView.as_view(), name='items'),
]
