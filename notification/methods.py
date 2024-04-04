from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from translation.methods import get_languages_codes
from notification.models import Notification


User = get_user_model()


def clean_notification_data(data: dict) -> dict:
    cleaned_data = {}
    for key, value in data.items():
        if value is not None:
            cleaned_data[key] = str(value)
    return cleaned_data


def _push_notifications(
        users: list,
        title: str,
        body: str,
        image: str,
        **data,
    ) -> None:
    data = clean_notification_data(data)
    FCMDevice.objects.filter(user__in=users).send_message(
        message=messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
                image=image,
            ),
            data=data,
        ),
    )


def save_notification(
        users: list,
        **data,
    ):
    notifications = [
        Notification(
            user=user,
            **data,
        ) 
        for user in users
    ]
    Notification.objects.bulk_create(notifications)


def validate_str_value(field, value):
    if not isinstance(value, str):
        raise ValidationError(f'{field} must be str.')


def validate_translated_field(notification_data, field):
    value = notification_data.get(field)
    if value:
        validate_str_value(field, value)
        return
    
    for code in get_languages_codes():
        field_code = f'{field}_{code}'
        value = notification_data.get(field_code)
        if not value:
            translated_fields = [f'{field}_{code}' for code in get_languages_codes()]
            raise ValidationError(f'if {field} is not provided then {translated_fields} are required.')
        validate_str_value(field_code, value)


def validate_notification_data(notification_data):
    validate_translated_field(notification_data, 'title')
    validate_translated_field(notification_data, 'body')
    validate_translated_field(notification_data, 'image')


def push_notifications(
        users: list,
        save: bool = True,
        **data,
    ):
    validate_notification_data(data)

    language_code_map = {}
    for user in users:
        language_code_map.setdefault(user.language_code, []).append(user)

    title = data.pop('title', None)
    body = data.pop('body', None)
    image = data.pop('image', None)
    for language_code, temp_users in language_code_map.items():
        _push_notifications(
            temp_users,
            title=data.get(f'title_{language_code}', title),
            body=data.get(f'body_{language_code}', body),
            image=data.get(f'image_{language_code}', image),
            **data,
        )
    
    if save:
        save_notification(
            users=users,
            title=title,
            body=body,
            image=image,
            **data,
        )
