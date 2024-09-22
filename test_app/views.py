from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet
from common.rest_framework.permissions import IsSuperuser
from users.verification.email import _send_verification_code_email_message
from users.verification.phone_number import _send_verification_code_phone_number_message, check_verification_code_phone_number
from .models import Test, SubTest
from .filters import UpdateTestFilter, GetTestFilter, SubTestFilter
from .serializers import (
    TestTimeModelSerializer,
    UpdateTestSerializer,
    ByFieldUpdateTestSerializer,
    GetTestSerializer,
    SubTestSerializer,
)

# --------------------------------------------------

class UpdateTestViewSet(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = UpdateTestSerializer
    filterset_class = UpdateTestFilter
    queryset = Test.objects.all()


class ByFieldUpdateTestViewSet(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = ByFieldUpdateTestSerializer
    filterset_class = UpdateTestFilter
    queryset = Test.objects.all()


class GetTestViewSet(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = GetTestSerializer
    filterset_class = GetTestFilter
    queryset = Test.objects.all()


class SubTestViewSet(ModelViewSet):
    permission_classes = (IsSuperuser,)
    serializer_class = SubTestSerializer
    filterset_class = SubTestFilter
    queryset = SubTest.objects.all()

# --------------------------------------------------

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

# --------------------------------------------------

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

# --------------------------------------------------

class ExceptionView(CreateAPIView):
    permission_classes = (IsSuperuser, )
    
    def create(self, request, *args, **kwargs):
        raise Exception('This is just an exception for testing.')
