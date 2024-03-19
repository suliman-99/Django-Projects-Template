from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from common.audit.serializers import AuditSerializer
from users.models import User
from users.validators import validate_user, validate_user_code
from users.methods import add_tokens_to_response, verify_email, verify_phone_number
from users.response_serializer import AuthUserSerializer
from users.common_error_messages import NOT_REGISTERED_USER, INCORRECT_LOGIN_DATA, INVALID_CODE
from users.verification.email import send_verification_code_email_message_to_user
from users.verification.phone_number import (
    send_verification_code_phone_number_message_to_user,
    check_verification_code_phone_number_to_user,
)


class SignUpSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = (
            'password',
            'email', 
            'phone_number',
            'first_name',
            'last_name',
        )

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validate_password(validated_data['password'])
        user = User.objects.create_user(**validated_data)
        user.send_verification_code_email_message()
        return AuthUserSerializer(user, context=self.context).data


class SendEmailVerificationCodeSerializer(serializers.Serializer):
    email = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, email=validated_data['email'])
        validate_user(user)
        send_verification_code_email_message_to_user(user)
        return {}


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.CharField()
    email_code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, email=validated_data['email'])
        validate_user(user)
        validate_user_code(user, 'email_code', validated_data['email_code'])        
        ret = AuthUserSerializer(user, context=self.context).data
        ret['reset_password_code'] = verify_email(user)
        return add_tokens_to_response(ret, user)


class EmailLogInSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(email=validated_data['email'])
        except User.DoesNotExist:
            raise ValidationError(NOT_REGISTERED_USER)
        
        validate_user(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        user.last_login = timezone.now()
        user.save()
        ret = AuthUserSerializer(user, context=self.context).data
        if user.email_verified:
            ret = add_tokens_to_response(ret, user)
        return ret


class SendPhoneNumberVerificationCodeSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, phone_number=validated_data['phone_number'])
        validate_user(user)
        send_verification_code_phone_number_message_to_user(user)
        return {}


class VerifyPhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        user = get_object_or_404(User, phone_number=validated_data['phone_number'])
        validate_user(user)
        if not check_verification_code_phone_number_to_user(user, validated_data['code']):
            raise ValidationError(INVALID_CODE)
        user.phone_number_verified = True
        user.last_login = timezone.now()
        user.save()
        ret = AuthUserSerializer(user, context=self.context).data
        ret['reset_password_code'] = verify_phone_number(user)
        return add_tokens_to_response(ret, user)


class PhoneNumberLogInSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        try:
            user = User.objects.get(phone_number=validated_data['phone_number'])
        except User.DoesNotExist:
            raise ValidationError(NOT_REGISTERED_USER)
        
        validate_user(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        user.last_login = timezone.now()
        user.save()
        ret = AuthUserSerializer(user, context=self.context).data
        if user.phone_number_verified:
            ret = add_tokens_to_response(ret, user)
        return ret
  

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
        
        user.last_refresh = timezone.now()
        user.save()
        ret = AuthUserSerializer(user, context=self.context).data
        return add_tokens_to_response(ret, user)


class ChagnePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        user:User = self.context['request'].user
        validate_user(user)

        if not check_password(validated_data['old_password'], user.password):
            raise ValidationError(_('Invalid password.'))
        
        validate_password(validated_data['password'])
        user.password = make_password(validated_data['password'])
        user.save()
        return AuthUserSerializer(user, context=self.context).data


class ReSetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    reset_password_code = serializers.CharField()

    def validate(self, attrs):
        validated_data =  super().validate(attrs)
        user:User = self.context['request'].user
        validate_user(user)
        validate_user_code(user, 'reset_password_code', validated_data['reset_password_code']) 
        validate_password(validated_data['password'])
        user.password = make_password(validated_data['password'])
        user.reset_password_code_is_valid = False
        user.save()
        return AuthUserSerializer(user, context=self.context).data


class ChangeEmailSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = ('email', )

    def update(self, user, validated_data):
        validated_data['email_verified'] = False
        ret = super().update(user, validated_data)
        send_verification_code_email_message_to_user(user)
        return ret
    
    def to_representation(self, user):
        return AuthUserSerializer(user, context=self.context).data


class ChangePhoneNumberSerializer(AuditSerializer):
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


class ProfileSerializer(AuditSerializer):
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


class FullUserSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'date_joined',
            'last_refresh',

            'email',
            'email_code',
            'email_code_time',
            'email_verified',

            'phone_number',
            'phone_number_verified',

            'reset_password_code',
            'reset_password_code_time',

            'first_name',
            'last_name',
            'language_code',

            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'deleted_at',
            'deleted_by',
            'is_deleted',
        )
        extra_kwargs = {
            'created_at': { 'read_only': True },
            'created_by': { 'read_only': True },
            'updated_at': { 'read_only': True },
            'updated_by': { 'read_only': True },
            'deleted_at': { 'read_only': True },
            'deleted_by': { 'read_only': True },
        }
