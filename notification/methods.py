from django.contrib.auth import get_user_model
from rest_framework import serializers
from firebase_admin import messaging
from fcm_django.models import FCMDevice
from common.audit.serializers import AuditSerializer
from translation.functions import get_default_language_code
from translation.plugs import TranslationSerializerPlug
from translation.fields import UpdateTranslationField
from notification.models import Notification


User = get_user_model()


def clean_notification_data(data):
    cleaned_data = {}
    for key, value in data.items():
        if value is not None:
            cleaned_data[key] = str(value)
    return cleaned_data


def save_notification(
        users,
        title,
        body,
        image,
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
    

class CreateTranslatedNotificationSerializer(TranslationSerializerPlug, AuditSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'title',
            'body',
            'image',
        )

    title = UpdateTranslationField()
    body = UpdateTranslationField()
    image = serializers.CharField()


def save_translated_notification(
        users,
        title,
        body,
        image,
    ):
    for user in users:
        serializer = CreateTranslatedNotificationSerializer(data={
            'user': user.id,
            'title': title,
            'body': body,
            'image': image,
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()


def push_notifications(
        users: list,
        title: str,
        body: str,
        image: str,
        save: bool = True,
        **data
    ):
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
    if save:
        save_notification(
            users=users,
            title=title,
            body=body,
            image=image,
        )


def push_translated_notifications(
        users: list,
        title: dict,
        body: dict,
        image: str,
        save: bool = True,
        **data
    ):
    default_language_code = get_default_language_code()
    default_title = title.get(default_language_code, '')
    default_body = body.get(default_language_code, '')

    language_code_map = {}
    for user in users:
        language_code_map.setdefault(user.language_code, []).append(user)

    for language_code, temp_users in language_code_map.items():
        push_notifications(
            temp_users,
            title=title.get(language_code, default_title),
            body=body.get(language_code, default_body),
            image=image,
            save=False,
            **data
        )

    if save:
        save_translated_notification(
            users=users,
            title=title,
            body=body,
            image=image,
        )
