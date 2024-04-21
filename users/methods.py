from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from common.code_generation import generate_code
from translation.methods import get_languages_codes, get_default_language_code
from users.models import User


def save_user(user: User, save: bool):
    if save:
        user.save()


def get_tokens(user: User, save: bool = True):
    user.last_refresh = timezone.now()
    save_user(user, save)
    refresh = TokenObtainPairSerializer.get_token(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def login(user: User, save: bool = True):
    user.first_login = user.first_login if user.first_login else timezone.now()
    user.last_login = timezone.now()
    tokens = get_tokens(user, False)
    save_user(user, save)
    return tokens


def verify(user: User, save: bool = True):
    reset_password_code = generate_code(20)
    user.reset_password_code = make_password(reset_password_code)
    user.reset_password_code_time = timezone.now()
    user.reset_password_code_is_valid = True
    save_user(user, save)
    return {
        'reset_password_code': reset_password_code,
    }


def verify_email(user: User, save: bool = True):
    tokens = login(user, False)
    reset_password_code = verify(user, False)
    user.email_code_is_valid = False
    user.email_verified = True
    save_user(user, save)
    return {
        **tokens, 
        **reset_password_code,
    }


def verify_phone_number(user: User, save: bool = True):
    tokens = login(user, False)
    reset_password_code = verify(user, False)
    user.phone_number_verified = True
    save_user(user, save)
    return {
        **tokens, 
        **reset_password_code,
    }


def get_user_language_code(user: User):
    return user.language_code if user.language_code in get_languages_codes() else get_default_language_code()


def get_permission_full_name(permission: Permission):
        return f'{permission.content_type.app_label}.{permission.codename}'
