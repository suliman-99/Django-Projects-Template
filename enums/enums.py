from .base.enum import BaseIntEnum


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
