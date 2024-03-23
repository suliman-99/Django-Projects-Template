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
