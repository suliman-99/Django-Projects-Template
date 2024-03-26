from django.contrib.auth.models import Permission, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import ModelPermissions, IsAdmin, IsSuperuser
from users.models import User
from users.filters import PermissionFilter
from users.serializers import (
    SignUpSerializer,
    SendEmailVerificationCodeSerializer,
    VerifyEmailSerializer,
    EmailLogInSerializer,
    SendPhoneNumberVerificationCodeSerializer,
    VerifyPhoneNumberSerializer,
    PhoneNumberLogInSerializer, 
    RefreshSerializer, 
    ChagnePasswordSerializer, 
    ReSetPasswordSerializer,
    ChangeEmailSerializer,
    ChangePhoneNumberSerializer,
    ProfileSerializer,
    FullUserSerializer,
    PermissionSerializer,
    GroupSerializer,
)

# ---------------------------------------- SignUp ----------------------------------------

class SignUpView(TokenObtainPairView):
    serializer_class = SignUpSerializer

# ---------------------------------------- Email ----------------------------------------

class ChangeEmailView(UpdateAPIView):
    serializer_class = ChangeEmailSerializer

    def get_object(self):
        return self.request.user


class SendEmailVerificationCodeView(TokenObtainPairView):
    serializer_class = SendEmailVerificationCodeSerializer


class VerifyEmailView(TokenObtainPairView):
    serializer_class = VerifyEmailSerializer


class EmailLogInView(TokenObtainPairView):
    serializer_class = EmailLogInSerializer

# ---------------------------------------- PhoneNumber ----------------------------------------

class ChangePhoneNumberView(UpdateAPIView):
    serializer_class = ChangePhoneNumberSerializer

    def get_object(self):
        return self.request.user


class SendPhoneNumberVerificationCodeView(TokenObtainPairView):
    serializer_class = SendPhoneNumberVerificationCodeSerializer


class VerifyPhoneNumberView(TokenObtainPairView):
    serializer_class = VerifyPhoneNumberSerializer


class PhoneNumberLogInView(TokenObtainPairView):
    serializer_class = PhoneNumberLogInSerializer

# ---------------------------------------- Common ----------------------------------------

class RefreshView(TokenObtainPairView):
    serializer_class = RefreshSerializer


class ChangePasswordView(TokenObtainPairView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = ChagnePasswordSerializer

    def get_object(self):
        return self.request.user


class ReSetPasswordView(TokenObtainPairView):
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = ReSetPasswordSerializer

    def get_object(self):
        return self.request.user

# ---------------------------------------- Profile ----------------------------------------

class ProfileView(RetrieveAPIView, UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

# ---------------------------------------- User ----------------------------------------

class UserViewSet(ModelViewSet):
    permission_models = User
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    serializer_class = FullUserSerializer
    queryset = User.objects.all() \
        .prefetch_related('user_permissions') \
        .prefetch_related('groups') \

# ---------------------------------------- Permission ----------------------------------------

class ProfilePermissionListAPIView(ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.prefetch_related('content_type')
    filterset_class = PermissionFilter

# ---------------------------------------- Group ----------------------------------------

class GroupViewSet(ModelViewSet):
    permission_models = Group
    permission_classes = ( (IsSuperuser | (IsAdmin & ModelPermissions)), )
    serializer_class = GroupSerializer
    queryset = Group.objects.all() \
        .prefetch_related('permissions') \
        .prefetch_related('user_set') \
            
# ---------------------------------------- END ----------------------------------------
