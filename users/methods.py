from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from common.code_generation import generate_code
from translation.cache import get_active_languages_codes, get_default_language_code
from users.models import User


def add_tokens_to_response(data, user: User):
    refresh = TokenObtainPairSerializer.get_token(user)
    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)
    return data


def verify_email(user: User):
    reset_password_code = generate_code(20)
    now = timezone.now()
    user.email_code_is_valid = False
    user.email_verified = True
    user.last_login = now
    user.reset_password_code = make_password(reset_password_code)
    user.reset_password_code_time = now
    user.reset_password_code_is_valid = True
    user.save()
    return reset_password_code


def verify_phone_number(user: User):
    reset_password_code = generate_code(20)
    now = timezone.now()
    user.phone_number_verified = True
    user.last_login = now
    user.reset_password_code = make_password(reset_password_code)
    user.reset_password_code_time = now
    user.reset_password_code_is_valid = True
    user.save()
    return reset_password_code


def get_user_language_code(user: User):
    return user.language_code if user.language_code in get_active_languages_codes() else get_default_language_code()
