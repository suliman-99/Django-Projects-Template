from django.contrib.contenttypes.models import ContentType
from common.audit.serializers import AuditSerializer


class ContentTypeSerializer(AuditSerializer):
    class Meta:
        model = ContentType
        fields = (
            'id', 
            'app_label', 
            'model',
        )
        