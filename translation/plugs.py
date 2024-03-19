import json
from translation.functions import get_active_languages_codes
from translation.fields import UpdateTranslationField


class TranslationSerializerPlug():
    """
    This Plug must be added as super class to any `Serializer` if it is wanted to save the tranlsation by `UpdateTranslationField`

    Additional:
    convert the data format to be saved if it is in the second format descriped in `to_internal_value()` method docstring below
    """
    def to_internal_value(self, data):
        """
        it converts the data from this format:

            {
                ...
                "field_name_language_code1": "value1",
                "field_name_language_code2": "value2"
                "field_name_language_code3": "value3"
                ...
            }

        to this format:

            {
                ...
                "field_name": {
                    "language_code1": "value1",
                    "language_code2": "value2"
                    "language_code3": "value3"
                }
                ...
            }
        """
        active_languages_codes = get_active_languages_codes()
        fields = [field for field in self.fields]
        deleted_fields = []
        added_fields = {}

        for field_name, value in data.items():
            if field_name in fields:
                if isinstance(value, str):
                    try:
                        value = json.loads(value)
                        data[field_name] = value
                    except:
                        pass
            else:
                for field in fields:
                    for active_language_code in active_languages_codes:
                        if field_name == f'{field}_{active_language_code}':
                            deleted_fields.append(field_name)
                            if not added_fields.get(field):
                                added_fields[field] = {}
                            added_fields[field][active_language_code] = value
        
        try:
            data._mutable = True
        except:
            pass

        for deleted_field in deleted_fields:
            data.pop(deleted_field)

        for key, value in added_fields.items():
            if not data.get(key):
                data[key] = {}
            data[key].update(**value)

        return super().to_internal_value(data)
    
    def run_custom_validation(self):
        """ this method calls the `run_validation()` method for all `UpdateTranslationField` objects in this serializer """
        for field_name, field in self.fields.items():
            if isinstance(field, UpdateTranslationField):
                field.run_custom_validation()
    
    def save_translations(self, instance):
        """ this method calls the `save_translations()` method for all `UpdateTranslationField` objects in this serializer """
        for field_name, field in self.fields.items():
            if isinstance(field, UpdateTranslationField):
                if self.initial_data.get(field_name):
                    field.save_translations(instance)

    def save(self, **kwargs):
        """ override the original `save() method to call `save_translation()` method in the end """
        self.run_custom_validation()
        instance = super().save(**kwargs)
        self.save_translations(instance)
        return instance
