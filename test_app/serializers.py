from django.utils import timezone
from rest_framework import serializers
from common.audit.serializers import AuditSerializer
from test_app.models import TestTimeModel


class TestTimeModelSerializer(AuditSerializer):
    class Meta:
        model = TestTimeModel
        fields = ('created_at', 'timezone_now', 'timezone_localtime_timezone_now')
        extra_kwargs = {
            'timezone_now': { 'read_only': True },
            'timezone_localtime_timezone_now': { 'read_only': True },
        }

    def create(self, validated_data):
        validated_data['timezone_now'] = timezone.now()
        validated_data['timezone_localtime_timezone_now'] = timezone.localtime(timezone.now())
        return super().create(validated_data)
