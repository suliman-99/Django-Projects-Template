from django.conf import settings


def get_languages():
    return [
        { 'code': code, 'name': name }
        for code, name in settings.LANGUAGES
    ]


def get_languages_codes():
    return [code for code, _ in settings.LANGUAGES]


def get_default_language_code():
    return settings.LANGUAGES[0][0]


def translate(name, value=None) -> list[str] | dict[str, any]:
    '''
    if value is None return ['name_en', 'name_ar',  ... ]
    else return {'name_en': value, 'name_ar': value,  ... }
    '''
    ret = [ f'{name}_{code}' for code in get_languages_codes() ]
    if value:
        ret = { name: value for name in ret }
    return ret


def translation_field_required_kwargs(name):
    return translate(name, { 'required': True, 'allow_null': False, 'allow_blank': False })
