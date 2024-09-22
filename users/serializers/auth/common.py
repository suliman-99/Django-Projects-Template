from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from ...models import User
from ...validators import validate_user, validate_user_code
from ...methods import get_tokens
from ...verification.email import send_verification_code_email_message_to_user
from ...verification.phone_number import send_verification_code_phone_number_message_to_user
from .base import AuthUserSerializer


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',
            'email', 
            'phone_number',

            'first_name',
            'last_name',
            'language_code',
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validate_password(validated_data['password'])
        user:User = User.objects.create_user(**validated_data)
        if user.email:
            send_verification_code_email_message_to_user(user)
        if user.phone_number:
            send_verification_code_phone_number_message_to_user(user)
        return AuthUserSerializer(user, context=self.context).data


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'language_code',
        )
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        refresh = validated_data.pop('refresh')
        refresh_obj = RefreshToken(refresh)
        refresh_obj.check_exp()

        try:
            user = User.objects.get(id=refresh_obj.payload.get('user_id'))
        except:
            raise AuthenticationFailed('Token  user_id is not found.')
        
        validate_user(user)
        
        ret = AuthUserSerializer(user, context=self.context).data
        ret.update(get_tokens(user))
        return ret


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'old_password',
            'password',
        )
    
    old_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        user:User = self.context['request'].user
        if not check_password(validated_data.pop('old_password'), user.password):
            raise ValidationError(_('Invalid password.'))
        validate_password(validated_data['password'])
        validated_data['password'] = make_password(validated_data['password'])
        return validated_data
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data


class ReSetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'reset_password_code',
            'password',
        )

    reset_password_code = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        user:User = self.context['request'].user
        validate_user_code(user, 'reset_password_code', validated_data.pop('reset_password_code')) 
        validate_password(validated_data['password'])
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['reset_password_code_is_valid'] = False
        return validated_data
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data
