from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from ...serializers.auth.common import (
    SignUpSerializer,
    RefreshSerializer,
    ChangePasswordSerializer,
    ReSetPasswordSerializer,
    UpdateProfileSerializer,
)
from .base import BaseAuthView


class SignUpView(BaseAuthView):
    serializer_class = SignUpSerializer


class ProfileView(RetrieveAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class RefreshView(BaseAuthView):
    serializer_class = RefreshSerializer


class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class ReSetPasswordView(UpdateAPIView):
    serializer_class = ReSetPasswordSerializer

    def get_object(self):
        return self.request.user
