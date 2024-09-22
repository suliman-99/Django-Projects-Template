import threading
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
from common.code_generation import generate_string_code
from ..models import User


def generate_email_verification_code():
    if settings.EMAIL_VERIFICATION_CODE_ALWAYS_123456:
        return '123456'
    return generate_string_code(6)


def _send_verification_code_email_message(name, code, to_email):
    send_mail(
        subject='Project_Name Email Verification Code', 
        html_message=render_to_string('verification_code_email.html', { 'name': name, 'verification_code': code }),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        message='',
    )


def send_verification_code_email_message(name, code, to_email):
    threading.Thread(target=_send_verification_code_email_message, args=(name, code, to_email)).start()


def send_verification_code_email_message_to_user(user: User):
    code = generate_email_verification_code()
    user.email_code = make_password(code)
    user.email_code_time = timezone.now()
    user.email_code_is_valid = True
    user.save()
    send_verification_code_email_message(user.email, code, user.email)
