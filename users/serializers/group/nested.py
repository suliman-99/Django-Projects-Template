from django.contrib.auth.models import Group
from rest_framework import serializers


class SmallGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id', 
            'name',
        )
