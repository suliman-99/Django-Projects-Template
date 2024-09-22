from .base.enum import BaseIntEnum, BaseEnum


class Status(BaseIntEnum):
    ACTIVE = 1
    INACTIVE = 0


class OsType(BaseIntEnum):
    ANDROID = 1
    IOS = 2
    WEB = 3
    WINDOWS = 4
    LINUX = 5
    MAC = 6


class Role(BaseIntEnum):
    SUPERUSER = 1
    ADMIN = 2


class Gender(BaseIntEnum):
    MALE = 1
    FEMALE = 2


class FCMType(BaseIntEnum):
    NOTIFICATION = 1
    MESSAGE = 2


class NotificationObjectType(BaseIntEnum):
    TYPE = 1


class NotificationTemplateType(BaseIntEnum):
    TYPE = 1
