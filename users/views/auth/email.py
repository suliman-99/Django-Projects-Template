
from rest_framework.generics import UpdateAPIView
from users.views.auth.base import BaseAuthView
from users.serializers.auth.email import (
    ChangeEmailSerializer,
    SendEmailVerificationCodeSerializer,
    VerifyEmailSerializer,
    EmailLogInSerializer,
)


class ChangeEmailView(UpdateAPIView):
    serializer_class = ChangeEmailSerializer

    def get_object(self):
        return self.request.user


class SendEmailVerificationCodeView(BaseAuthView):
    serializer_class = SendEmailVerificationCodeSerializer


class VerifyEmailView(BaseAuthView):
    serializer_class = VerifyEmailSerializer


class EmailLogInView(BaseAuthView):
    serializer_class = EmailLogInSerializer
