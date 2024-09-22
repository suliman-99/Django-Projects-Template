from common.audit.serializer import AuditSerializer
from .models import Item


class ItemSerializer(AuditSerializer):
    class Meta:
        model = Item
        fields = (
            'file',
        )
    
    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)
