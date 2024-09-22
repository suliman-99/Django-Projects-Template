from rest_framework.generics import UpdateAPIView
from ...serializers.auth.phone_number import (
    ChangePhoneNumberSerializer,
    SendPhoneNumberVerificationCodeSerializer,
    VerifyPhoneNumberSerializer,
    PhoneNumberLogInSerializer,
)
from .base import BaseAuthView


class ChangePhoneNumberView(UpdateAPIView):
    serializer_class = ChangePhoneNumberSerializer

    def get_object(self):
        return self.request.user


class SendPhoneNumberVerificationCodeView(BaseAuthView):
    serializer_class = SendPhoneNumberVerificationCodeSerializer


class VerifyPhoneNumberView(BaseAuthView):
    serializer_class = VerifyPhoneNumberSerializer


class PhoneNumberLogInView(BaseAuthView):
    serializer_class = PhoneNumberLogInSerializer
