from rest_framework import serializers
from translation.methods import translate
from system_info.models import SystemInfo


class AdminSystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = (
            *translate('privacy_policy'), 
            *translate('term_of_us'), 
            *translate('about_us'),
        )


class SystemInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemInfo
        fields = (
            'privacy_policy', 
            'term_of_us', 
            'about_us',
        )
        