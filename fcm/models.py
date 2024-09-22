from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from fcm_django.models import AbstractFCMDevice
from common.audit.models import HistoricalAuditModel
from enums.enums import Role


User = get_user_model()


class CustomFCMDevice(HistoricalAuditModel, AbstractFCMDevice):
    registration_id = models.CharField(max_length=500, verbose_name=_("Registration token"), unique=True)
    role = models.IntegerField(choices=Role.choices)
