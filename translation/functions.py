"""
This field contains method to cach the languages and the translations records in the needed way
Provide methods to get and set translations values
"""
from django.core.cache import cache
from content_type.cache import get_content_type_id_by_object
from translation.models import Language, Translation


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


def get_language_code_from_request(request):
    language_code = request.headers.get('Accept-Language')
    if not language_code:
        language_code = get_default_language_code()
    return language_code


# --------------------------------------------------------------------------------------------------------- #
# -------------------- These Two Functions have to be integrated correctly -------------------------------- #
# --------------------------------------------------------------------------------------------------------- #
                                                                                                            #
def make_translation_object_key(tr_obj):                                                                    #
    """ make the translation dict key from a translation object """                                         #
    return ( tr_obj.content_type_id, tr_obj.object_id, tr_obj.field_name, tr_obj.language_code )            #
                                                                                                            #
                                                                                                            #
def make_object_key(obj, field_name, language_code):                                                        #
    """ make the translation dict key from an object with its field_name and language_code needed """       #
    return ( get_content_type_id_by_object(obj), str(obj.id), field_name, language_code )                   #
                                                                                                            #
# --------------------------------------------------------------------------------------------------------- #


TRANSLATION_KEY = 'TRANSLATION_KEY'


def load_translations():
    """ cache the translations as a dict[key: translation dict key, value: translation object] """
    data = { 
        make_translation_object_key(tr_obj): tr_obj 
        for tr_obj in Translation.objects.all() 
    }
    cache.set(TRANSLATION_KEY, data, timeout=300)


def get_translations():
    """ get the translations dict """
    data = cache.get(TRANSLATION_KEY)
    if data is None:
        load_translations()
        data = cache.get(TRANSLATION_KEY)
    return data


def process_object_field(obj, field_name):
    parts = field_name.split('.')
    field_name = parts[-1]
    parts = parts[:-1]
    for part in parts:
        obj = getattr(obj, part)
    return obj, field_name


def get_translation_object(obj, field_name, language_code):
    """ get a specific object from the translations dict """
    obj, field_name = process_object_field(obj, field_name)
    key = make_object_key(obj, field_name, language_code)
    return get_translations().get(key)


def get_all_translations_objects_for_object_field(obj, field_name):
    """ get all translation objects for a specific (object-field) """
    active_languages_codes = get_active_languages_codes()
    tr_objs = {}
    for language_code in active_languages_codes:
        tr_obj = get_translation_object(obj, field_name, language_code)
        tr_objs[language_code] = tr_obj
    return tr_objs


def fall_down_from_model(obj, field_name):
    return getattr(obj, field_name)


def fall_down_from_default_language_then_from_model(obj, field_name):
    return get_translation_value(
        obj, 
        field_name, 
        get_default_language_code(), 
        fall_down_from_model,
    )


def fall_down_from_default_language_then_empty(obj, field_name):
    return get_translation_value(
        obj, 
        field_name, 
        get_default_language_code(), 
        '',
    )


def get_fall_down_value(obj, field_name, fall_down):
    if callable(fall_down):
        return fall_down(obj, field_name)
    return fall_down


def get_translation_value_from_object(obj, field_name, fall_down, tr_obj):
    return tr_obj.value if tr_obj else get_fall_down_value(obj, field_name, fall_down)


def get_translation_value(obj, field_name, language_code, fall_down):
    """ get a specific translation value from the translations dict """
    tr_obj = get_translation_object(obj, field_name, language_code)
    return get_translation_value_from_object(obj, field_name, fall_down, tr_obj)


def get_all_translations_values_for_object_field(obj, field_name, fall_down):
    """ get all translation values for a specific (object-field) """
    return { 
        key: get_translation_value_from_object(obj, field_name, fall_down, tr_obj) 
        for key, tr_obj in get_all_translations_objects_for_object_field(obj, field_name).items() 
    }


def set_translations_for_object_field(obj, field_name, translations):
    """ set all translations for a specific (object-field) """
    obj, field_name = process_object_field(obj, field_name)
    for language_code, value in translations.items():
        translation, _ = Translation.objects.get_or_create(
            content_type_id=get_content_type_id_by_object(obj), 
            object_id=obj.id, 
            field_name=field_name, 
            language_code=language_code,
        )
        translation.value = value
        translation.save()
