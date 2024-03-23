from django.contrib.auth import get_user_model
from rest_framework import serializers
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from translation.fields import UpdateTranslationField
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
        **data
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
        title: dict,
        body: dict,
        image: str,
    ):
    notifications = [
        Notification(
            user=user,
            title=title,
            body=body,
            image=image,
        ) 
        for user in users
    ]
    Notification.objects.bulk_create(notifications)
    

class ValidateTranslatedNotificationSerializer(serializers.Serializer):
    title = UpdateTranslationField(base_is_enough=True)
    body = UpdateTranslationField(base_is_enough=True)
    image = serializers.CharField()


def push_notifications(
        users: list,
        title: dict | str,
        body: dict | str,
        image: str,
        save: bool = True,
        **data
    ):
    serializer = ValidateTranslatedNotificationSerializer(data={
        'title': title,
        'body': body,
        'image': image,
    })
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    title = validated_data['title']
    body = validated_data['body']
    image = validated_data['image']

    language_code_map = {}
    for user in users:
        language_code_map.setdefault(user.language_code, []).append(user)

    title_base = title.get('base')
    body_base = body.get('base')
    for language_code, temp_users in language_code_map.items():
        _push_notifications(
            temp_users,
            title=title.get(language_code, title_base),
            body=body.get(language_code, body_base),
            image=image,
            **data
        )
    
    if save:
        save_notification(
            users=users,
            title=title,
            body=body,
            image=image,
        )
