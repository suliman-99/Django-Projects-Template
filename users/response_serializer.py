from common.audit.serializers import AuditSerializer
from users.models import User


class AuthUserSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
            'last_refresh',

            'email',
            'email_verified',

            'phone_number',
            'phone_number_verified',

            'first_name',
            'last_name',
            'language_code',
        )  
