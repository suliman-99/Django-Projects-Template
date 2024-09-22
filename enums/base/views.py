from rest_framework import response
from rest_framework import exceptions
from rest_framework import generics, viewsets
from rest_framework import permissions
from .serializers import EnumSerializer, EnumModelSerializer
from .filters import EnumModelFilter


class BaseForEnumModel:
    permission_classes = (permissions.AllowAny, )
    filterset_class = EnumModelFilter
    serializer_class = EnumModelSerializer

    def get_queryset(self):
        return self.model.objects.all()


class EnumModelReadOnlyView(
        BaseForEnumModel, 
        generics.ListAPIView,
        generics.RetrieveAPIView
    ):
    pass


class EnumModelReadOnlyViewSet(
        BaseForEnumModel, 
        viewsets.ReadOnlyModelViewSet
    ):
    pass

# ----------------------------------------------------------------------------

class BaseForEnum:
    permission_classes = (permissions.AllowAny, )
    
    def retrieve(self, request, *args, **kwargs):
        for o in self.enum:
            if str(o.value) == self.kwargs['pk']:
                return response.Response(EnumSerializer(o, context=self.get_serializer_context()).data)
        raise exceptions.NotFound()
    
    def list(self, request, *args, **kwargs):
        return response.Response(EnumSerializer(self.enum, many=True, context=self.get_serializer_context()).data)


class EnumReadOnlyView(
        BaseForEnum, 
        generics.ListAPIView,
        generics.RetrieveAPIView,
    ):
    pass


class EnumReadOnlyViewSet(
        BaseForEnum, 
        viewsets.ReadOnlyModelViewSet,
    ):
    pass
