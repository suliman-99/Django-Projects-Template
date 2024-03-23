from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from translation.methods import get_languages


class LanguageListAPIView(ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(get_languages())
