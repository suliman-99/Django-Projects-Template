from django.conf import settings
from firebase_admin import messaging
from enums.enums import FCMType
from .models import CustomFCMDevice


FCM_TYPE_NOTIFICATION = 1
FCM_TYPE_MESSAGE = 2

FCM_TYPE = 'FCM_TYPE'


def clean_data(data: dict):
    return {
        key: str(value) for key, value in data.items()
        if value
    }


def _push_for_users(users, role, data, notification=None):
    if not settings.ACTIVATE_FIREBASE:
        return
    data = clean_data(data)
    return CustomFCMDevice.objects.filter(user__in=users, role=role).send_message(
        message=messaging.Message(
            data=data,
            notification=notification,
        ),
    )


def _push_notifications_for_users(
        users: list,
        role: int,
        title: str,
        body: str,
        image: str,
        data: dict,
    ) -> None:
    data = { FCM_TYPE: FCMType.NOTIFICATION, **data }
    notification = messaging.Notification(title=title, body=body, image=image)
    return _push_for_users(users=users, role=role, data=data, notification=notification)


def _push_messages_for_users(
        users: list,
        role: int,
        data: dict,
    ) -> None:
    data = { FCM_TYPE: FCMType.MESSAGE, **data }
    return _push_for_users(users=users, role=role, data=data, notification=None)
