from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.audit.serializers import AuditSerializer
from translation.fields import GetTranslationField
from translation.functions import fall_down_from_model
from translation.plugs import TranslationSerializerPlug
from translation.fields import UpdateTranslationField
from notification.models import Notification
from notification.methods import push_notifications


User = get_user_model()


class FilterSerializer(serializers.Serializer):
    user_ids = serializers.ListField(required=True, allow_null=True, child=serializers.CharField())
    is_excepting = serializers.BooleanField(required=True)


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    body = serializers.CharField(required=True)
    image = serializers.CharField(required=True, allow_null=True)


class SendNotificationSerializer(serializers.Serializer):
    filter = FilterSerializer()
    notification = NotificationSerializer()
    save = serializers.BooleanField()

    def get_users(self, filter_data):
        user_ids = filter_data.get('user_ids')
        is_excepting = filter_data.get('is_excepting')

        filter = Q()
        if user_ids:
            filter &= Q(id__in=user_ids)
        if is_excepting:
            filter = ~filter

        return User.objects.filter(filter)

    def create(self, validated_data):
        filter_data = validated_data['filter']
        notification_data = validated_data['notification']
        save = validated_data['save']
        users = self.get_users(filter_data)
        push_notifications(
            users, 
            title=notification_data.pop('title'),
            body=notification_data.pop('body'),
            image=notification_data.pop('image'),
            save=save,
            **notification_data
        )
        return True
    
    def to_representation(self, instance):
        return {}


class GetNotificationSerializer(AuditSerializer):
    class Meta:
        model = Notification
        fields = (
            'id', 
            'title', 
            'body', 
            'image', 
            'is_viewed', 
            'created_at',
        )

    title = GetTranslationField(fall_down=fall_down_from_model)
    body = GetTranslationField(fall_down=fall_down_from_model)


class MarkNotificationAsViewedSerializer(AuditSerializer):
    class Meta:
        model = Notification
        fields = []

    def update(self, instance, validated_data):
        instance.is_viewed = True
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return GetNotificationSerializer(instance, context=self.context).data
    

class FullNotificationSerializer(TranslationSerializerPlug, AuditSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'is_viewed',

            'title',
            'body',
            'image',

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

    title = UpdateTranslationField()
    body = UpdateTranslationField()
