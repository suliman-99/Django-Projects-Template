from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsSuperuser
from users.models import User
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

# ---------------------------------------- Superuser ----------------------------------------

class UserViewSet(ModelViewSet):
    permission_classes = (IsSuperuser, )
    serializer_class = FullUserSerializer
    queryset = User.objects.all()

# ---------------------------------------- End ----------------------------------------
