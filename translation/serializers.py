from common.audit.serializers import AuditSerializer
from translation.models import Language


class LanguageSerializer(AuditSerializer):
    class Meta:
        model = Language
        fields = (
            'id', 
            'name', 
            'native_name', 
            'code', 
            'is_active', 
            'is_default',
        )
