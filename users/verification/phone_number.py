import threading
from django.conf import settings
from twilio.rest import Client
from users.models import User


def _send_verification_code_phone_number_message(to_phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    to = '+' + to_phone_number

    return client.verify \
        .v2 \
        .services(settings.TWILIO_SERVICE) \
        .verifications \
        .create(to=to, channel='sms')


def send_verification_code_phone_number_message(to_phone_number):
    if settings.ACTIVATE_TWILIO:
        threading.Thread(target=_send_verification_code_phone_number_message, args=(to_phone_number, )).start()


def send_verification_code_phone_number_message_to_user(user: User):
    send_verification_code_phone_number_message(user.phone_number)


def check_verification_code_phone_number(to_phone_number, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    to = '+' + to_phone_number

    return client.verify \
        .v2 \
        .services(settings.TWILIO_SERVICE) \
        .verification_checks \
        .create(to=to, code=code)


def check_verification_code_phone_number_to_user(user: User, code):
    check_verification_code_phone_number(user.phone_number, code)
