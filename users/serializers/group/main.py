from django.contrib.auth.models import Group
from rest_framework import serializers
from ..permission import PermissionSerializer
from ..user.nested import SmallUserSerializer


class GetFullGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 
            'name', 
            'permissions', 
            'user_set',
            'user_count',
            'permission_count',
        )

    permissions = PermissionSerializer(many=True)
    permission_count = serializers.SerializerMethodField()

    user_set = SmallUserSerializer(many=True)
    user_count = serializers.SerializerMethodField()

    def get_permission_count(self, instance):
        return len(instance.permissions.all())

    def get_user_count(self, instance):
        return len(instance.user_set.all())


class UpdateFullGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 
            'name', 
            'permissions', 
            'user_set',
        )

    def to_representation(self, instance):
        return GetFullGroupSerializer(instance, context=self.context).data
