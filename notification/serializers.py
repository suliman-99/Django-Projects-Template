from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.audit.serializer import AuditSerializer
from translation.methods import translate, translation_field_required_kwargs
from .models import Notification, NotificationTemplate
from .methods import push_notifications


User = get_user_model()


class FilterSerializer(serializers.Serializer):
    user_ids = serializers.ListField(required=True, allow_null=True, child=serializers.CharField())

    is_active = serializers.BooleanField(required=False, allow_null=True)
    # is_superuser = serializers.BooleanField(required=False, allow_null=True)
    # is_staff = serializers.BooleanField(required=False, allow_null=True)

    is_excepting = serializers.BooleanField(required=True)


class SendNotificationSerializer(serializers.Serializer):
    filter = FilterSerializer()
    save = serializers.BooleanField()
    notification = serializers.JSONField()

    def get_users(self, filter_data):
        user_ids = filter_data.pop('user_ids', None)
        is_excepting = filter_data.pop('is_excepting', None)

        filter = Q()

        if user_ids:
            filter &= Q(id__in=user_ids)

        if filter_data:
            filter &= Q(**filter_data)
            
        if is_excepting:
            filter = ~filter

        return User.objects.filter(filter)

    def create(self, validated_data):
        push_notifications(
            users=self.get_users(validated_data.pop('filter')),
            save=validated_data['save'],
            **validated_data['notification'],
        )
        return True
    
    def to_representation(self, instance):
        return {}


class GetNotificationSerializer(AuditSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 
            'user',
            'role',
            'title', 
            'body', 
            'image', 
            'object_type',
            'object_id',
            'extra_data',
            'is_viewed', 
            'created_at',
            'updated_at',
        )


class FullNotificationSerializer(AuditSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'role',
            'title',
            'body',
            'image',
            'object_type',
            'object_id',
            'extra_data',
            'is_viewed',
            'created_at',
            'updated_at',
        )


class NotificationTemplateSerializer(AuditSerializer):
    class Meta:
        model = NotificationTemplate
        fields = (
            'id',

            'type',

            *translate('title'),
            *translate('body'),
            *translate('image'),

            'extra_data',
        )
        extra_kwargs = {
            **translation_field_required_kwargs('title'),
            **translation_field_required_kwargs('body'),
        }
