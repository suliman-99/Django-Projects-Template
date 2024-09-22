from rest_framework import serializers


class AuditSerializer(serializers.ModelSerializer):
    def get_user(self):
        user = self.context['request'].user
        if not user or not user.is_authenticated:
            user = None
        return user

    def create(self, validated_data):
        validated_data['created_by'] = self.get_user()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['updated_by'] = self.get_user()
        return super().update(instance, validated_data)
