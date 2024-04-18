from translation.fields import UpdateTranslationField
from rest_framework import serializers


class JsonTranslationPlug(serializers.ModelSerializer):
    @property
    def validated_data(self):
        for field in self.fields.values():
            if isinstance(field, UpdateTranslationField):
                field.add_outer_values(self._validated_data)
        return super().validated_data
