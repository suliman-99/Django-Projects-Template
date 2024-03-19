from datetime import datetime
from django.utils import timezone
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from common.permissions import IsSuperuser
from users.verification.email import _send_verification_code_email_message
from users.verification.phone_number import _send_verification_code_phone_number_message, check_verification_code_phone_number
from test_app.serializers import TestTimeModelSerializer


class TestSendEmailVerificationCode(CreateAPIView):
    permission_classes = (IsSuperuser, )
    
    def create(self, request, *args, **kwargs):
        name = request.data['name']
        code = request.data['code']
        to_email = request.data['to_email']
        _send_verification_code_email_message(name, code, to_email)
        return Response({})


class TestSendPhoneNumberVerificationCode(CreateAPIView):
    permission_classes = (IsSuperuser, )

    def create(self, request, *args, **kwargs):
        to_phone_number = request.data['to_phone_number']
        res = _send_verification_code_phone_number_message(to_phone_number)
        return Response({ 'status': str(res.status) })


class TestVerifyPhoneNumber(CreateAPIView):
    permission_classes = (IsSuperuser, )

    def create(self, request, *args, **kwargs):
        to_phone_number = request.data['to_phone_number']
        code = request.data['code']
        res = check_verification_code_phone_number(to_phone_number, code)
        return Response({ 'status': str(res.status) })


class TestTime(RetrieveAPIView):
    permission_classes = (IsSuperuser, )
    
    def retrieve(self, request, *args, **kwargs):
        datetime_now = datetime.now()
        timezone_now = timezone.now()
        timezone_localtime_timezone_now = timezone.localtime(timezone.now())
        is_equal = (timezone_now == timezone_localtime_timezone_now)
        return Response({
            'datetime_now': str(datetime_now),
            'timezone_now': str(timezone_now),
            'timezone_localtime_timezone_now': str(timezone_localtime_timezone_now),
            'is_equal': is_equal,
        })
    

class TestTimeModelViewSet(ModelViewSet):
    permission_classes = (IsSuperuser, )
    serializer_class = TestTimeModelSerializer
