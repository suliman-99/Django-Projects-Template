from rest_framework import serializers


class CustomImageField(serializers.ImageField):
    def to_representation(self, value):
        if value.name.startswith('http'):
            return value.name
        return super().to_representation(value)
