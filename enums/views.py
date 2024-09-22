from .base.views import EnumReadOnlyViewSet
from .enums import (
    OsType, 
    Role,
    Gender,
    FCMType,
)


class OsTypeReadOnlyViewSet(EnumReadOnlyViewSet):
    enum = OsType


class RoleReadOnlyViewSet(EnumReadOnlyViewSet):
    enum = Role


class GenderReadOnlyViewSet(EnumReadOnlyViewSet):
    enum = Gender


class FCMTypeReadOnlyViewSet(EnumReadOnlyViewSet):
    enum = FCMType
