from django.urls import path
from rest_framework import routers
from .views.permission import PermissionViewSet
from .views.group import GroupViewSet
from .views.user import UserViewSet
from .views.auth.common import (
    SignUpView,
    ProfileView,
    RefreshView,
    ChangePasswordView,
    ReSetPasswordView,
)
from .views.auth.email import (
    ChangeEmailView,
    SendEmailVerificationCodeView,
    VerifyEmailView,
    EmailLogInView,
)
from .views.auth.phone_number import (
    ChangePhoneNumberView,
    SendPhoneNumberVerificationCodeView,
    VerifyPhoneNumberView,
    PhoneNumberLogInView,
)


router = routers.DefaultRouter()

router.register('permissions', PermissionViewSet, 'permissions')
router.register('groups', GroupViewSet, 'groups')
router.register('users', UserViewSet, 'users')

urlpatterns = router.urls + [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', ReSetPasswordView.as_view(), name='reset-password'),
    
    path('change-email/', ChangeEmailView.as_view(), name='change-email'),
    path('send-email-verification-code/', SendEmailVerificationCodeView.as_view(), name='send-email-verification-code'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('email-login/', EmailLogInView.as_view(), name='email-login'),
    
    path('change-phone-number/', ChangePhoneNumberView.as_view(), name='change-phone-number'),
    path('send-phone-number-verification-code/', SendPhoneNumberVerificationCodeView.as_view(), name='send-phone-number-verification-code'),
    path('verify-phone-number/', VerifyPhoneNumberView.as_view(), name='verify-phone-number'),
    path('phone-number-login/', PhoneNumberLogInView.as_view(), name='phone-number-login'),
]
