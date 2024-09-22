from django.conf import settings
from firebase_admin import messaging
from enums.enums import FCMType
from .models import CustomFCMDevice


FCM_TYPE = 'FCM_TYPE'


def _push_for_users(users, role, data, notification=None):
    if not settings.ACTIVATE_FIREBASE:
        return
    CustomFCMDevice.objects.filter(user__in=users, role=role).send_message(
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
    _push_for_users(users=users, role=role, data=data, notification=notification)


def _push_messages_for_users(
        users: list,
        role: int,
        data: dict,
    ) -> None:
    data = { FCM_TYPE: FCMType.MESSAGE, **data }
    _push_for_users(users=users, role=role, data=data, notification=None)
