import copy
import json
from rest_framework import exceptions
from translation.functions import get_active_languages_codes
from translation.fields import UpdateTranslationField


def coordinate_translation_initial_data(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except:
            pass
    return data


def validate_translation_initial_data(field_name, data):
    if data is not None and not isinstance(data, dict):
        raise exceptions.ValidationError({field_name: 'This field must be a json object.'})


class TranslationSerializerPlug():
    """
    This Plug must be added as super class to any `Serializer` if it is wanted to save the tranlsation by `UpdateTranslationField`

    Additional:
    convert the data format to be saved if it is in the second format descriped in `to_internal_value()` method docstring below
    """
    def get_fields_names(self):
        if not getattr(self, 'fields_names', None):
            self.fields_names = list(self.fields.keys())
        return self.fields_names

    def get_translation_fields_names(self):
        if not getattr(self, 'translation_fields_names', None):
            self.translation_fields_names = [
                field_name 
                for field_name, field in self.fields.items()
                if isinstance(field, UpdateTranslationField)
            ]
        return self.translation_fields_names
    
    def get_action(self):
        try:
            return self.context['view'].action
        except:
            return 'update'
    
    def save_translation_data(self, data):
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
        then save it in `translation_data` attribute
        """
        fields_names = self.get_fields_names()
        translation_fields_names = self.get_translation_fields_names()
        active_languages_codes = get_active_languages_codes()
        self.translation_data = {}

        for field_name, value in data.items():
            if field_name in fields_names:
                if field_name in translation_fields_names:
                    value = coordinate_translation_initial_data(value)
                    validate_translation_initial_data(field_name, value)
                self.translation_data[field_name] = value

        for field_name, value in data.items():
            if field_name not in fields_names:
                for translation_field_name in translation_fields_names:
                    for active_language_code in active_languages_codes:
                        if field_name == f'{translation_field_name}_{active_language_code}':
                            self.translation_data.setdefault(translation_field_name, {})[active_language_code] = value

    def to_internal_value(self, data):
        self.save_translation_data(copy.deepcopy(data))
        return super().to_internal_value(data)
    
    def run_custom_validation(self):
        """ this method calls the `run_validation()` method for all `UpdateTranslationField` objects in this serializer """
        action = self.get_action()
        for translation_field_name in self.get_translation_fields_names():
            translation_field = self.fields[translation_field_name]
            translations = self.translation_data.get(translation_field_name)
            translation_field.run_custom_validation(translations, action)
    
    def save_translations(self, instance):
        """ this method calls the `save_translations()` method for all `UpdateTranslationField` objects in this serializer """
        for translation_field_name in self.get_translation_fields_names():
            translations = self.translation_data.get(translation_field_name)
            if translations:
                translation_field = self.fields[translation_field_name]
                translation_field.save_translations(instance, translations)

    def save(self, **kwargs):
        """ override the original `save() method to call `save_translation()` method in the end """
        self.run_custom_validation()
        instance = super().save(**kwargs)
        self.save_translations(instance)
        return instance
