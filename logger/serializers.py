from rest_framework import serializers
from logger.models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = (
            'id',
            'created_at',
            'level',
            'type',
            'user',
            'method',
            'url',
            'message',
            'html_message',
            'query_params',
            'request_headers',
        )
