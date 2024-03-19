from django.urls import path
from rest_framework import routers
from test_app.views import (
    TestSendEmailVerificationCode,
    TestSendPhoneNumberVerificationCode,
    TestVerifyPhoneNumber,
    TestTime,
    TestTimeModelViewSet,
)

router = routers.DefaultRouter()

router.register('test-time-model', TestTimeModelViewSet, 'test-time-model')

urlpatterns = router.urls + [
    path('test-send-email-verification-code/', TestSendEmailVerificationCode.as_view(), name='test-send-email-verification-code'),
    path('test-send-phone-number-verification-code/', TestSendPhoneNumberVerificationCode.as_view(), name='test-send-phone-number-verification-code'),
    path('test-verify-phone-number/', TestVerifyPhoneNumber.as_view(), name='test-verify-phone-number'),
    path('test-time/', TestTime.as_view(), name='test-time'),
]
