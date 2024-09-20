from django.conf import settings
    

def get_field_name(field_name, language_code):
    if language_code == 'base':
        return field_name
    return f'{field_name}_{language_code}'


def get_languages():
    return [
        { 'code': code, 'name': name }
        for code, name in settings.LANGUAGES
    ]


def get_languages_codes(with_base=False) -> list[str]:
    languages_codes = (code for code, _ in settings.LANGUAGES)
    if with_base:
        languages_codes = ('base', *languages_codes)
    return list(languages_codes)


def get_default_language_code():
    return settings.MODELTRANSLATION_DEFAULT_LANGUAGE


def translate(name, value=None, with_base=False) -> list[str] | dict[str, any]:
    ret = [ get_field_name(name, code) for code in get_languages_codes(with_base) ]
    if value:
        return { key: value for key in ret }
    return ret


def full_translate(name, value=None) -> list[str] | dict[str, any]:
    return translate(name, value, True)


def translation_field_required_kwargs(name, with_base=False):
    return translate(name, { 'required': True, 'allow_null': False, 'allow_blank': False }, with_base)


def full_translation_field_required_kwargs(name):
    return translation_field_required_kwargs(name, True)


def get_field_translation_data_as_json(data, field_name):
    return {
        language_code: data.get(get_field_name(field_name, language_code))
        for language_code in get_languages_codes(with_base=True)
    }
