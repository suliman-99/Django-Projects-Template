from translation.fields import UpdateTranslationField


class FromJsonTranslationPlug():
    def validate(self, data):
        for field in self.fields.values():
            if isinstance(field, UpdateTranslationField):
                field.add_outer_values(data)
        validated_data = super().validate(data)
        return validated_data
