from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from translation.functions import get_active_languages_codes
from users.common_error_messages import INACTIVE_USER
from users.models import User


def validate_user(user):
    if not user.is_active:
        raise ValidationError(INACTIVE_USER)
    

def validate_language_code(language_code):
    if language_code not in get_active_languages_codes:
        raise ValidationError('Invalid Language Code.')
    

def validate_user_code(user: User, code_name, code):
    user_code = getattr(user, code_name)
    user_code_time = getattr(user, f'{code_name}_time')
    user_code_is_valid = getattr(user, f'{code_name}_is_valid')

    if not user_code or not user_code_time:
        raise ValidationError(_('Send Code Before Verifying It.'))

    if timezone.now() - user_code_time > timezone.timedelta(seconds=300):
        raise ValidationError(_('Old Code.'))

    if not user_code_is_valid:
        raise ValidationError(_('Used Code.'))

    if not check_password(code, user_code):
        raise ValidationError(_('Invalid Code.'))
