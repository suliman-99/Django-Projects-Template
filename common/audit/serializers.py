from django.utils import timezone
from rest_framework import serializers


class AuditSerializer(serializers.ModelSerializer):
    def get_user(self):
        try:
            user = self.context['request'].user
        except:
            return None
        if not user or not user.is_authenticated:
            return None
        return user

    def create(self, validated_data):
        user = self.get_user()
        validated_data['created_by'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.get_user()
        validated_data['updated_by'] = user
        if validated_data.get('is_deleted') == True and not instance.is_deleted:
            validated_data['deleted_by'] = user
            validated_data['deleted_at'] = timezone.now()
        return super().update(instance, validated_data)
