from rest_framework import serializers
from common.audit.serializer import AuditSerializer
from translation.methods import get_default_language_code, full_translate
from translation.fields import UpdateTranslationField
from translation.plugs import JsonTranslationPlug
from users.methods import get_user_language_code
from fcm.methods import _push_notifications_for_users
from .models import Notification, NotificationTemplate


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


class NotificationSerializer(JsonTranslationPlug, serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'role',
            'title',
            'body',
            'image',
            'object_type',
            'object_id',
            'extra_data',
        )

    title = UpdateTranslationField(base_is_enough=True)
    body = UpdateTranslationField(base_is_enough=True)
    image = UpdateTranslationField(required_languages=[])


def push_notifications(
        users: list,
        save: bool = True,
        **data,
    ):
    notification_serializer = NotificationSerializer(data=data)
    notification_serializer.is_valid(raise_exception=True)
    validated_notification_data = notification_serializer.validated_data

    language_code_map = {}
    for user in users:
        language_code_map.setdefault(get_user_language_code(user), []).append(user)

    title = validated_notification_data.get('title', None)
    body = validated_notification_data.get('body', None)
    image = validated_notification_data.get('image', None)

    role = validated_notification_data.get('role')

    for language_code, temp_users in language_code_map.items():
        _push_notifications_for_users(
            users=temp_users,
            role=role,
            title=validated_notification_data.get(f'title_{language_code}', title),
            body=validated_notification_data.get(f'body_{language_code}', body),
            image=validated_notification_data.get(f'image_{language_code}', image),
            data=validated_notification_data,
        )

    if save:
        save_notification(
            users=users,
            **validated_notification_data,
        )


def default_translated_push_notifications(
        users: list,
        save: bool = True,
        **data,
    ):
    default_language_code = get_default_language_code()
    data.setdefault('title', data.get(f'title_{default_language_code}'))
    data.setdefault('body', data.get(f'body_{default_language_code}'))
    data.setdefault('image', data.get(f'image_{default_language_code}'))
    push_notifications(
        users=users,
        save=save,
        **data,
    )


class NotificationTemplateDataExtractorSerializer(AuditSerializer):
    class Meta:
        model = NotificationTemplate
        fields = (
            *full_translate('title'),
            *full_translate('body'),
            *full_translate('image'),

            'extra_data',
        )


def get_notification_template_by_type(type):
    return NotificationTemplate.objects.filter(type=type).first()


def push_notification_by_template(template, users, role, object_type, object_id):
    if template:
        push_notifications(
            users=users,
            role=role,
            object_type=object_type,
            object_id=str(object_id),
            **NotificationTemplateDataExtractorSerializer(template).data,
        )


def push_notification_by_type(type, users, role, object_type, object_id):
    push_notification_by_template(
        template=get_notification_template_by_type(type),
        users=users,
        role=role,
        object_type=object_type,
        object_id=object_id,
    )
