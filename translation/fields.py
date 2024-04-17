import json
from django.utils.translation import get_language
from rest_framework import serializers, exceptions
from translation.methods import get_field_name, get_languages_codes, get_default_language_code


def coordinate_string_json(translation_data):
        if isinstance(translation_data, str):
            try:
                translation_data = json.loads(translation_data)
            except:
                translation_data = {'base': translation_data}
        return translation_data


def validate_translation_data_is_json(translation_data, field_name):
    if not isinstance(translation_data, dict):
        raise exceptions.ValidationError({field_name: f'{field_name} must be key-value json.'})


def get_from_outer_values(serializer_initial_data, translation_data, field_name):
    for key, value in serializer_initial_data.items():
        for language_code in get_languages_codes():
            if key == get_field_name(field_name, language_code):
                translation_data[language_code] = value


def ensure_base_value(translation_data):
    translation_data.setdefault('base', translation_data.get(get_default_language_code(), ''))


def validate_translation_data(
        field_name,
        accepted_languages,
        required_languages,
        base_is_enough,
        allow_partial,
        translation_data,
    ):
    missed_language_codes = []
    invalid_language_codes = []
    
    if not allow_partial and not (base_is_enough and translation_data.get('base')):
        for language_code in required_languages:
            if not translation_data.get(language_code):
                missed_language_codes.append(language_code)

    
    accepted_keys = ['base', *accepted_languages]
    for key in translation_data.keys():
        if key not in accepted_keys:
            invalid_language_codes.append(key)

    error_messages = []
    if missed_language_codes:
        error_messages.append(f'missed language codes: {missed_language_codes}')
    if invalid_language_codes:
        error_messages.append(f'invalid language codes: {invalid_language_codes}')

    if error_messages:
        raise exceptions.ValidationError({
            field_name: ', '.join(error_messages) + f' in {field_name}',
        })


class UpdateTranslationField(serializers.SerializerMethodField):
    def __init__(self, 
        allow_partial=False,
        base_is_enough=False,
        required_languages=get_languages_codes(),
        accepted_languages=get_languages_codes(),
        **kwargs
    ):
        self.allow_partial = allow_partial
        self.base_is_enough = base_is_enough
        self.required_languages = required_languages
        self.accepted_languages = accepted_languages

        if not all(o in self.accepted_languages for o in self.required_languages):
            raise Exception('required_languages must be a part of the accepted_languages')
        
        super().__init__(**kwargs)

    def get_validated_translation_data(self):
        initial_data = self.parent.initial_data
        translation_data = initial_data.get(self.field_name)
        translation_data = coordinate_string_json(translation_data)
        validate_translation_data_is_json(translation_data, self.field_name)
        get_from_outer_values(initial_data, translation_data, self.field_name)
        ensure_base_value(translation_data)
        validate_translation_data(
            self.field_name,
            self.accepted_languages,
            self.required_languages,
            self.base_is_enough,
            self.allow_partial,
            translation_data,
        )
        return translation_data
    
    def add_outer_values(self, data):
        translation_data = self.get_validated_translation_data()
        return data.update({
            get_field_name(self.field_name, language_code): value
            for language_code, value in translation_data.items()
        })

    def to_representation(self, instance):
        return {
            language_code: getattr(instance, get_field_name(self.field_name, language_code))
            for language_code in get_languages_codes(True)
        }
