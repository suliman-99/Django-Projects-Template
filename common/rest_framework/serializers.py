from rest_framework import serializers


class CustomFileSerializerField(serializers.ImageField):
    def to_representation(self, value):
        if value and value.name.startswith('http'):
            return value.name
        return super().to_representation(value)
