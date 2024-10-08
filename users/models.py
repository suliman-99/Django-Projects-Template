import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.contrib.auth.hashers import make_password
from phonenumber_field.modelfields import PhoneNumberField
from safedelete.managers import SafeDeleteManager
from common.audit.models import HistoricalAuditModel


class UserManager(SafeDeleteManager, BaseUserManager):
    def create_user(self, **data):
        data['password'] = make_password(data['password'])
        if data.get('email'):
            data['email'] = self.normalize_email(data['email'])
        return super().create(**data)
    
    def create_superuser(self, **data):
        data['is_superuser'] = True
        data['is_staff'] = True
        data['is_admin'] = True
        data['email_verified'] = True
        data['phone_number_verified'] = True
        return self.create_user(**data)


class User(AbstractUser, HistoricalAuditModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=False, null=True, blank=True)
    first_login = models.DateTimeField(null=True, blank=True)
    last_refresh = models.DateTimeField(null=True, blank=True)
     
    email = models.CharField(max_length=255, null=True, blank=True)
    email_code = models.CharField(max_length=500, null=True, blank=True)
    email_code_time = models.DateTimeField(null=True, blank=True)
    email_code_is_valid = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    phone_number = PhoneNumberField(null=True, blank=True)
    phone_number_verified = models.BooleanField(default=False)

    reset_password_code = models.CharField(max_length=500, null=True, blank=True)
    reset_password_code_time = models.DateTimeField(null=True, blank=True)
    reset_password_code_is_valid = models.BooleanField(default=False)

    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    language_code = models.CharField(max_length=10, null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f'({self.id} - {self.email} - {self.phone_number})'

    class Meta(AbstractUser.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                condition=models.Q(deleted__isnull=True),
                name='unique_active_email',
            ),
            models.UniqueConstraint(
                fields=['phone_number'],
                condition=models.Q(deleted__isnull=True),
                name='unique_active_phone_number',
            ),
        ]
