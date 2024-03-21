from rest_framework import serializers
from logger.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            'id',
            'type',
            'user',
            'status_code',
            'method',
            'url',
            'query_params',
            'request_headers',
            'request_body',
            'response_headers',
            'response_body',
            'created_at',
        )
