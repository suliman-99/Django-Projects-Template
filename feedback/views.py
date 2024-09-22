from rest_framework.viewsets import ModelViewSet
from common.rest_framework.permissions import IsAdmin, ModelPermissions
from .models import Feedback
from .serializers import FeedbackSerializer


class FeedbackViewSet(ModelViewSet):
    http_method_names = ['post']
    serializer_class = FeedbackSerializer


class AdminFeedbackViewSet(ModelViewSet):
    http_method_names = ['get']
    permission_classes = (IsAdmin, ModelPermissions)
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
