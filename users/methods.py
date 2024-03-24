from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from common.code_generation import generate_code
from translation.methods import get_languages_codes, get_default_language_code
from users.models import User


def get_tokens(user: User):
    user.last_refresh = timezone.now()
    refresh = TokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def login(user: User):
    user.first_login = user.first_login if user.first_login else timezone.now()
    user.last_login = timezone.now()
    return get_tokens(user)


def verify(user: User):
    reset_password_code = generate_code(20)
    user.reset_password_code = make_password(reset_password_code)
    user.reset_password_code_time = timezone.now()
    user.reset_password_code_is_valid = True
    return {
        'reset_password_code': reset_password_code,
    }


def verify_email(user: User):
    tokens = login(user)
    reset_password_code = verify(user)
    user.email_code_is_valid = False
    user.email_verified = True
    user.save()
    return {
        **tokens, 
        **reset_password_code,
    }


def verify_phone_number(user: User):
    tokens = login(user)
    reset_password_code = verify(user)
    user.phone_number_verified = True
    user.save()
    return {
        **tokens, 
        **reset_password_code,
    }


def get_user_language_code(user: User):
    return user.language_code if user.language_code in get_languages_codes() else get_default_language_code()
