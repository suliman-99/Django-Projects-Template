import json
from django.utils.translation import get_language
from rest_framework import serializers, exceptions
from common.dicts import DefaultDict
from translation.methods import get_languages_codes, get_default_language_code


def fallback_to_base(data):
    return data.get('base', '')


def fallback_to_default_language_then_to_empty(data):
    return data.get(get_default_language_code(), '')


def fallback_to_default_language_then_to_base(data):
    return data.get(get_default_language_code(), fallback_to_base(data))


def coordinate_translation_data(data):
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                data = {'base': data}
        return data


def ensure_base_value(translation_data):
    translation_data.setdefault('base', translation_data.get(get_default_language_code()))


class TranslationField(serializers.JSONField):
    """ 
    The `TranslationField` class provides a minimal class which may be used
    for writing custom tranlsation implementations.
    
    Note: it is subclasse of `JSONField`
    """

    def __init__(self, **kwargs):
        """
        - `fallback` attribute is a method takes (obj, field_name) or a value specify what will be returned if the a translation value is not available
        """
        self.fallback = kwargs.pop('fallback', '')
        super().__init__(**kwargs)

    def get_fallback_value(self, data):
        if not callable(self.fallback):
            return self.fallback
        return self.fallback(data)
    
    def to_representation(self, value):
        data = super().to_representation(value)
        if not isinstance(data, dict):
            data = {}
        return DefaultDict(self.get_fallback_value(data), data)


class GetTranslationField(TranslationField):
    """ 
    The `GetTranslationField` class  is a subclasse of `TranslationField`

    GET:
        It returns the translated value of the field depending on the `Accept-Language` entered in the header.
        `Accept-Language` values must be `Language.code` field values.  

        if there is no translation value related to the `Accept-Language` specified
        then, it will return the value depending on the fallback 
    """
    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)
    
    def to_representation(self, value):
        data = super().to_representation(value)
        language_code = get_language()
        return data[language_code]


class UpdateTranslationField(TranslationField):
    """
    The `UpdateTranslationField` class  is a subclasse of `TranslationField`

    GET:
        It returns all translation values of the field in this format:
        "field_name": {
            "language_code1": "value1",
            "language_code2": "value2"
            "language_code3": "value3"
        }
        it will return the object for all languages_codes
        if there is no translation value related to the any of the languages
        then, it will return the value depending on the fallback
     
    SET:
        it accept the data in this format:
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

    def __init__(self, **kwargs):
        """
        - `allow_partial` attribute which make the field accept the value even that not all languages are specified if `allow_partial`=True
        - `base_is_enough` attribute is a flag that specify if the value of `base` key is enough in validations
        """
        self.allow_partial = kwargs.pop('allow_partial', False)
        self.base_is_enough = kwargs.pop('base_is_enough', False)
        super().__init__(**kwargs)
    
    def validate_translation_data(self, translation_data):
        if not isinstance(translation_data, dict):
            raise exceptions.ValidationError({self.field_name: f'{self.field_name} must be key-value json.'})
        
        languages_codes = get_languages_codes()
        required_language_codes = []
        invalid_language_codes = []
        
        if not self.allow_partial and not (self.base_is_enough and translation_data.get('base')):
            for language_code in languages_codes:
                if not translation_data.get(language_code):
                    required_language_codes.append(language_code)

        accepted_keys = ['base', *languages_codes]
        for key in translation_data.keys():
            if key not in accepted_keys:
                invalid_language_codes.append(key)

        error_messages = []
        if required_language_codes:
            error_messages.append(f'required language codes: {required_language_codes}')
        if invalid_language_codes:
            error_messages.append(f'invalid language codes: {invalid_language_codes}')

        if error_messages:
            raise exceptions.ValidationError({
                self.field_name: ', '.join(error_messages) + f' in {self.field_name}',
            })

    def to_internal_value(self, translation_data):
        translation_data = super().to_internal_value(translation_data)
        translation_data = coordinate_translation_data(translation_data)
        ensure_base_value(translation_data)
        self.validate_translation_data(translation_data)
        return translation_data

    def to_representation(self, value):
        data = super().to_representation(value)
        new_data = {
            language_code: data[language_code]
            for language_code in get_languages_codes()
        }
        new_data['base'] = data.get('base', '')
        return new_data
