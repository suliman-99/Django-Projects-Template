from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from rest_framework import serializers
from common.audit.variables import audit_fields, audit_read_only_kwargs
from translation.methods import full_translate
from notification.models import Notification
from notification.methods import push_notifications


User = get_user_model()


class FilterSerializer(serializers.Serializer):
    user_ids = serializers.ListField(required=True, allow_null=True, child=serializers.CharField())
    is_excepting = serializers.BooleanField(required=True)


class SendNotificationSerializer(serializers.Serializer):
    filter = FilterSerializer()
    save = serializers.BooleanField()
    notification = serializers.JSONField()

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
        push_notifications(
            users=self.get_users(validated_data['filter']),
            save=validated_data['save'],
            **validated_data['notification'],
        )
        return True
    
    def to_representation(self, instance):
        return {}


class GetNotificationSerializer(serializers.ModelSerializer):
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


class MarkNotificationAsViewedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = []

    def update(self, instance, validated_data):
        instance.is_viewed = True
        instance.save()
        return instance
    
    def to_representation(self, instance):
        return GetNotificationSerializer(instance, context=self.context).data
    

class FullNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'is_viewed',

            *full_translate('title'),
            *full_translate('body'),
            *full_translate('image'),
            
            *audit_fields,
        )
        extra_kwargs = {
            **audit_read_only_kwargs
        }
