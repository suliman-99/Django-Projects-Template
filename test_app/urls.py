from django.urls import path
from rest_framework import routers
from test_app.views import (
    TestSendEmailVerificationCode,
    TestSendPhoneNumberVerificationCode,
    TestVerifyPhoneNumber,
    TestTime,
    TestTimeModelViewSet,
    ExceptionView,
    UpdateTestViewSet,
    ByFieldUpdateTestViewSet,
    GetTestViewSet,
    SubTestViewSet,
)

router = routers.DefaultRouter()

router.register('test-time-model', TestTimeModelViewSet, 'test-time-model')
router.register('update-test', UpdateTestViewSet, 'update-test')
router.register('by-field-update-test', ByFieldUpdateTestViewSet, 'by-field-update-test')
router.register('test', GetTestViewSet, 'test')
router.register('sub-test', SubTestViewSet, 'sub-test')

urlpatterns = router.urls + [
    path('test-send-email-verification-code/', TestSendEmailVerificationCode.as_view(), name='test-send-email-verification-code'),
    path('test-send-phone-number-verification-code/', TestSendPhoneNumberVerificationCode.as_view(), name='test-send-phone-number-verification-code'),
    path('test-verify-phone-number/', TestVerifyPhoneNumber.as_view(), name='test-verify-phone-number'),
    path('test-time/', TestTime.as_view(), name='test-time'),
    path('exception/', ExceptionView.as_view(), name='exception'),
]
