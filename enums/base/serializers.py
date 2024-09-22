from rest_framework import serializers


class EnumSerializer(serializers.Serializer):
    value = serializers.CharField()
    label = serializers.CharField()


class EnumModelSerializer(serializers.Serializer):
    def to_representation(self, instance):
        return instance.name
