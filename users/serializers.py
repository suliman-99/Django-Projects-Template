from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from common.audit.serializers import AuditSerializer
from common.audit.variables import audit_fields, audit_read_only_kwargs
from content_type.serializers import ContentTypeSerializer
from users.models import User
from users.validators import validate_user, validate_user_code
from users.methods import get_tokens, login, verify_email, verify_phone_number
from users.response_serializer import AuthUserSerializer
from users.common_error_messages import NOT_REGISTERED_USER, INCORRECT_LOGIN_DATA, INVALID_CODE
from users.verification.email import send_verification_code_email_message_to_user
from users.verification.phone_number import (
    send_verification_code_phone_number_message_to_user,
    check_verification_code_phone_number_to_user,
)

# ---------------------------------------- SignUp ----------------------------------------

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
        if not validated_data['email'] and not validated_data['phone_number']:
            raise ValidationError('Email or Phone Number are required.')
        user:User = User.objects.create_user(**validated_data)
        if user.email:
            send_verification_code_email_message_to_user(user)
        if user.phone_number:
            send_verification_code_phone_number_message_to_user(user)
        return AuthUserSerializer(user, context=self.context).data

# ---------------------------------------- Email ----------------------------------------

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
        
        validate_user(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        ret = AuthUserSerializer(user, context=self.context).data
        if user.email_verified:
            ret.update(login(user))
        return ret

# ---------------------------------------- PhoneNumber ----------------------------------------

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
        
        validate_user(user)
        
        if not check_password(validated_data['password'], user.password):
            raise ValidationError(INCORRECT_LOGIN_DATA)

        ret = AuthUserSerializer(user, context=self.context).data
        if user.phone_number_verified:
            ret.update(login(user))
        return ret
  
# ---------------------------------------- Common ----------------------------------------

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

# ---------------------------------------- Profile ----------------------------------------

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

# ---------------------------------------- User ----------------------------------------

class FullUserSerializer(AuditSerializer):
    class Meta:
        model = User
        fields = (
            'id',

            'password',
            
            'is_active',
            'is_staff',
            'is_superuser',
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
        extra_kwargs = {
            'password': { 'write_only': True, 'allow_null': True },
            'date_joined': { 'read_only': True },
            'first_login': { 'read_only': True },
            'last_login': { 'read_only': True },
            'last_refresh': { 'read_only': True },
            'email_code_time': { 'read_only': True },
            'email_code_is_valid': { 'read_only': True },
            'reset_password_code_time': { 'read_only': True },
            'reset_password_code_is_valid': { 'read_only': True },
            **audit_read_only_kwargs
        }
    
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        return validated_data

# ---------------------------------------- Permission ----------------------------------------

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            'id', 
            'name', 
            'codename', 
            'full_name',
            'content_type', 
        )

    full_name = serializers.SerializerMethodField()
    content_type = ContentTypeSerializer()

    def get_full_name(self, instance):
        return f'{instance.content_type.app_label}.{instance.codename}'

# ------------------------------------------------- Group -------------------------------------------------

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 
            'name', 
            'permissions', 
            'user_set',
        )

# ------------------------------------------------- END -------------------------------------------------
