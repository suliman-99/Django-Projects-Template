from django.contrib.auth import get_user_model
from rest_framework import serializers
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from translation.methods import get_default_language_code
from translation.fields import UpdateTranslationField
from translation.plugs import JsonTranslationPlug
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
        data: dict,
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
        data: dict,
    ):
    notifications = [
        Notification(
            user=user,
            **data,
        ) 
        for user in users
    ]
    Notification.objects.bulk_create(notifications)


class NotificationSerializer(JsonTranslationPlug, serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'title',
            'body',
            'image',
            'is_viewed',
            'created_at',
        )

    title = UpdateTranslationField(base_is_enough=True)
    body = UpdateTranslationField(base_is_enough=True)
    image = UpdateTranslationField(required_languages=[])


def push_notifications(
        users: list,
        data: dict,
        save: bool = True,
    ):
    notification_serializer = NotificationSerializer(data=data)
    notification_serializer.is_valid(raise_exception=True)
    validated_notification_data = notification_serializer.validated_data

    language_code_map = {}
    for user in users:
        language_code_map.setdefault(user.language_code, []).append(user)

    title = validated_notification_data.get('title', None)
    body = validated_notification_data.get('body', None)
    image = validated_notification_data.get('image', None)
    for language_code, temp_users in language_code_map.items():
        _push_notifications(
            temp_users,
            title=validated_notification_data.get(f'title_{language_code}', title),
            body=validated_notification_data.get(f'body_{language_code}', body),
            image=validated_notification_data.get(f'image_{language_code}', image),
            data=validated_notification_data,
        )
    
    if save:
        save_notification(
            users=users,
            data=validated_notification_data,
        )


def default_translated_push_notifications(
        users: list,
        data: dict,
        save: bool = True,
    ):
    default_language_code = get_default_language_code()
    data.setdefault('title', data.get(f'title_{default_language_code}'))
    data.setdefault('body', data.get(f'body_{default_language_code}'))
    data.setdefault('image', data.get(f'image_{default_language_code}'))
    push_notifications(
        users=users,
        data=data,
        save=save,
    )
