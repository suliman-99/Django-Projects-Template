from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache


CONTENT_TYPE_KEY = 'CONTENT_TYPE_KEY'


def load_content_types():
    content_types_list = list(ContentType.objects.all())
    content_types_map = { obj.model: obj for obj in content_types_list }
    data = {
        'list': content_types_list,
        'map': content_types_map,
    }
    cache.set(CONTENT_TYPE_KEY, data, timeout=300)


def get_content_types_data():
    data = cache.get(CONTENT_TYPE_KEY)
    if data is None:
        load_content_types()
        data = cache.get(CONTENT_TYPE_KEY)
    return data


def get_content_types_list():
    return get_content_types_data()['list']


def get_content_types_map():
    return get_content_types_data()['map']


def get_content_type_object_by_table_name(table_name):
    return get_content_types_map().get(table_name)


def get_content_type_object_by_object(obj):
    return get_content_type_object_by_table_name(obj._meta.model_name)


def get_content_type_id_by_table_name(table_name):
    obj = get_content_type_object_by_table_name(table_name)
    try:
        id = obj.id
    except:
        id = None
    return id


def get_content_type_id_by_object(obj):
    return get_content_type_id_by_table_name(obj._meta.model_name)
