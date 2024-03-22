from rest_framework import serializers, exceptions
from translation.functions import (
    get_active_languages_codes,
    get_default_language_code,
    get_language_code_from_request,
    get_translation_value,
    get_all_translations_values_for_object_field,
    set_translations_for_object_field,
)


class TranslationField(serializers.SerializerMethodField):
    """ 
    The `TranslationField` class provides a minimal class which may be used
    for writing custom tranlsation implementations.
    
    Note: it is subclasse of `SerializerMethodField`

    Additional args:
        source:
            This arg specify the real `field_name` in the model like and it will be sotored in the `custom_source` attribute
    """

    def __init__(self, **kwargs):
        """
        - `source` in an attribute called `custom_source` it works like the source attribute in the serializer fields
        - `allow_partial` attribute which make the field accept the value even that not all languages are specified if `allow_partial`=True
        - `fall_down` attribute is a method takes (obj, field_name) or a value specify what will be returned if the needed translation value is not available

        Note: saving it in the source will cause errors
        because `SerializerMethodField` cant have a source value
        """
        self.allow_partial = kwargs.pop('allow_partial', False)
        self.custom_source = kwargs.pop('source', None)
        self.fall_down = kwargs.pop('fall_down', '')
        super().__init__(**kwargs)

    def get_custom_source(self):
        """ return the `custom_source` arg value if it is provided in `source` value or the `field_name` """
        return self.custom_source or self.field_name


class GetTranslationField(TranslationField):
    """ 
    The `GetTranslationField` class  is a subclasse of `TranslationField`

    GET:
        It returns the translated value of the field depending on the `Accept-Language` entered in the header.
        `Accept-Language` values must be `Language.code` field values.  

        if there is no translation value related to the object and field_name and `Accept-Language` specified
        then, it will return the value stored in the origin object field (value from the model field) 
    """

    def to_representation(self, instance):
        """ return the translated value """
        return get_translation_value(
            instance, 
            self.get_custom_source(), 
            get_language_code_from_request(self.context['request']),
            self.fall_down,
        )


class UpdateTranslationField(TranslationField):
    """
    The `UpdateTranslationField` class  is a subclasse of `TranslationField`

    Note: it needs to be used inside a serializer extends `TranslationSerializerPlug` to do the save implementation
     
    GET:
        It returns all translation values of the field in this format:
        "field_name": {
            "language_code1": "value1",
            "language_code2": "value2"
        }
        it will return the object for all language_codes
        the value will be `Empty String` for any language_code if there is no related translation value
     
    SET:
        It sets all translation values of the field:

            it accept the data in this format originally:
                {
                    ...
                    "field_name": {
                        "language_code1": "value1",
                        "language_code2": "value2"
                        "language_code3": "value3"
                    }
                    ...
                }

            Another Formats can be accepted by `TranslationSerializerPlug` (it will be converted to the original format):
                {
                    ...
                    "field_name_language_code1": "value1",
                    "field_name_language_code2": "value2"
                    "field_name_language_code3": "value3"
                    ...
                }

            or combination of them together like this:
                {
                    ...
                    "field_name": {
                        "language_code1": "value1",
                        "language_code2": "value2"
                    },
                    "field_name_language_code3": "value3"
                    ...
                }
    """

    def to_representation(self, instance):
        """ return all the tranlations values """
        ret = get_all_translations_values_for_object_field(
            instance, 
            self.get_custom_source(),
            self.fall_down,
        )
        ret['in_table'] = getattr(instance, self.get_custom_source())
        return ret

    def run_custom_validation(self, translations, action):
        """
        - validate that all language_code are sent
        - validate that all language_code sent in the data are valid
        """
        if not translations:
            if self.allow_null or action == 'partial_update':
                return
            raise exceptions.ValidationError({
                self.field_name: f'{self.field_name} is required.'
            })
        
        if not isinstance(translations, dict):
            raise exceptions.ValidationError({self.field_name: f'{self.field_name} must be key-value json.'})
        
        active_languages_codes = get_active_languages_codes()
        needed_language_codes = []
        invalid_language_codes = []
        
        if not self.allow_partial:
            for language_code in active_languages_codes:
                if not translations.get(language_code):
                    needed_language_codes.append(language_code)

        for key in translations.keys():
            if key not in ['in_table', *active_languages_codes]:
                invalid_language_codes.append(key)

        error_messages = []
        if needed_language_codes:
            error_messages.append(f'needed language codes: {needed_language_codes}')
        if invalid_language_codes:
            error_messages.append(f'invalid language codes: {invalid_language_codes}')

        if error_messages:
            raise exceptions.ValidationError({
                self.field_name: ', '.join(error_messages) + f' in {self.field_name}',
            })
        
    def save_in_table_value(self, instance, translations):
        in_table = translations.get('in_table')
        if not in_table:
            in_table = translations.get(get_default_language_code())
        if in_table:
            setattr(instance, self.get_custom_source(), in_table)
            instance.save()
    
    def save_translations(self, instance, translations):
        """
        save all the tanslation values in `Translation` Table using `set_translations_for_object_field()` 
        
        this field class is a subclass of the SerializerMethodField
        so, validation will remove the data and will not return it in the validated_data
        so, get the data from the `serializer.inital_date` to save it
        """
        set_translations_for_object_field(instance, self.get_custom_source(), translations)
        self.save_in_table_value(instance, translations)
    