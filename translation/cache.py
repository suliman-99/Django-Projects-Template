"""
This field contains method to cach the languages and the translations records in the needed way
Provide methods to get and set translations values
"""
from django.core.cache import cache
from translation.models import Language


LANGUAGES_KEY = 'LANGUAGES_KEY'


def load_languages():
    """ cache the languages as list of objects """
    data = list(Language.objects.all())
    cache.set(LANGUAGES_KEY, data, timeout=300)


def get_languages():
    """ get the languages objects list """
    data = cache.get(LANGUAGES_KEY)
    if data is None:
        load_languages()
        data = cache.get(LANGUAGES_KEY)
    return data


def get_active_languages():
    """ get the active languages objects list """
    languages = get_languages()
    active_languages = []
    for language in languages:
        if language.is_active:
            active_languages.append(language)
    return active_languages


def get_active_languages_codes():
    """ get the active languages codes list """
    return [language.code for language in get_active_languages()]


def get_default_language():
    for language in get_active_languages():
        if language.is_default:
            return language


def get_default_language_code():
    return get_default_language().code
