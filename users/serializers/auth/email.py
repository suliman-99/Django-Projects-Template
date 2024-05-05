from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User
from users.validators import validate_email_login, validate_user_code
from users.methods import login, verify_email
from users.serializers.auth.base import AuthUserSerializer
from users.common_error_messages import NOT_REGISTERED_USER, INCORRECT_LOGIN_DATA
from users.verification.email import send_verification_code_email_message_to_user


class ChangeEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def update(self, user, validated_data):
        validated_data['email'] = User.objects.normalize_email(validated_data['email'])
        validated_data['email_verified'] = False
        ret = super().update(user, validated_data)
        send_verification_code_email_message_to_user(user)
        return ret
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data


class SendEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, email=validated_data['email'])
        validate_email_login(user)
        send_verification_code_email_message_to_user(user)
        return {}


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    email_code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, email=validated_data['email'])
        validate_email_login(user)
        validate_user_code(user, 'email_code', validated_data['email_code'])        
        ret = AuthUserSerializer(user, context=self.context).data
        ret.update(verify_email(user))
        return ret


class EmailLogInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            raise ValidationError(NOT_REGISTERED_USER)
        
        validate_email_login(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        ret = AuthUserSerializer(user, context=self.context).data
        if user.email_verified:
            ret.update(login(user))
        return ret
