from rest_framework.permissions import AllowAny
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer


class ItemCreateAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
