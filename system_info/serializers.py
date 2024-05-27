from rest_framework import serializers
from system_info.models import SystemInfo


class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = (
            'privacy_policy', 
            'term_of_us', 
            'about_us',
        )
        