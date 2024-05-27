from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User
from users.validators import validate_phone_number_login
from users.methods import login, verify_phone_number
from users.serializers.auth.base import AuthUserSerializer
from users.common_error_messages import NOT_REGISTERED_USER, INCORRECT_LOGIN_DATA, INVALID_CODE
from users.verification.phone_number import (
    send_verification_code_phone_number_message_to_user,
    check_verification_code_phone_number_to_user,
)


class ChangePhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number', )

    def update(self, user, validated_data):
        validated_data['phone_number_verified'] = False
        ret = super().update(user, validated_data)
        send_verification_code_phone_number_message_to_user(user)
        return ret
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data


class SendPhoneNumberVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, phone_number=validated_data['phone_number'])
        validate_phone_number_login(user)
        send_verification_code_phone_number_message_to_user(user)
        return {}


class VerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, phone_number=validated_data['phone_number'])
        validate_phone_number_login(user)
        if not check_verification_code_phone_number_to_user(user, validated_data['code']):
            raise ValidationError(INVALID_CODE)
        
        ret = AuthUserSerializer(user, context=self.context).data
        ret.update(verify_phone_number(user))
        return ret


class PhoneNumberLogInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(phone_number=validated_data['phone_number'])
        except User.DoesNotExist:
            raise ValidationError(NOT_REGISTERED_USER)
        
        validate_phone_number_login(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        ret = AuthUserSerializer(user, context=self.context).data
        if user.phone_number_verified:
            ret.update(login(user))
        else:
            send_verification_code_phone_number_message_to_user(user)
        return ret
