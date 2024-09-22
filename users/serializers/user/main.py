from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from common.audit.variables import audit_fields
from ...models import User
from ..group.nested import SmallGroupSerializer
from ..permission import PermissionSerializer


class GetFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            
            'is_active',
            'is_admin',

            'date_joined',
            'first_login',
            'last_login',
            'last_refresh',

            'email',
            'email_code_time',
            'email_code_is_valid',
            'email_verified',

            'phone_number',
            'phone_number_verified',

            'reset_password_code_time',
            'reset_password_code_is_valid',

            'first_name',
            'last_name',
            'language_code',

            'user_permissions',
            'groups',
            
            *audit_fields,
        )

    user_permissions = PermissionSerializer(many=True)
    groups = SmallGroupSerializer(many=True)


class UpdateFullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',

            'password',
            
            'is_active',
            'is_admin',
            
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
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        
        password = validated_data.pop('password', None)
        email = validated_data.pop('email', None)
        
        if password:
            validated_data['password'] = make_password(password)
        if email:
            validated_data['email'] = User.objects.normalize_email(email)
        
        return validated_data
    
    def to_representation(self, instance):
        return GetFullUserSerializer(instance, context=self.context).data
