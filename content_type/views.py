from rest_framework.viewsets import ModelViewSet
from .serializers import ContentTypeSerializer
from .cache import get_content_types_list


class ContentTypeViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = []
    serializer_class = ContentTypeSerializer
    
    def get_queryset(self):
        return get_content_types_list()
