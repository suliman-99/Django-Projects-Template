from rest_framework import serializers
from .models import User


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            
            'is_active',
            'is_staff',
            'is_superuser',
            'is_admin',

            'date_joined',
            'first_login',
            'last_login',
            'last_refresh',

            'email',
            'email_verified',

            'phone_number',
            'phone_number_verified',

            'first_name',
            'last_name',
            'language_code',

            'user_permissions',
            'groups',
        )  
