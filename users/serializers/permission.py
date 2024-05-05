from django.contrib.auth.models import Permission
from rest_framework import serializers
from content_type.serializers import ContentTypeSerializer
from users.methods import get_permission_full_name


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
        return get_permission_full_name(instance)
