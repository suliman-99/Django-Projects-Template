from rest_framework.viewsets import ModelViewSet
from common.permissions import IsSuperuserOrReadOnly
from translation.models import Language
from translation.serializers import LanguageSerializer


class LanguageViewSet(ModelViewSet):
    permission_classes = (IsSuperuserOrReadOnly, )
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
