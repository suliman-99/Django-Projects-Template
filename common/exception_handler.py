from rest_framework import status
from rest_framework.views import exception_handler


def message_coordinator(message, field_name):
    return message \
        .replace('blank', 'null') \
        .replace('may not be null', 'is required') \
        .replace('This', field_name) \
        .replace("_id", "") \
        .replace("_", " ") \
        .capitalize() \


def get_first_error_message(detail):
    if isinstance(detail, dict):
        for key, value in detail.items():
            field_name, message = get_first_error_message(value)
            if not field_name:
                field_name = key
            return field_name, message_coordinator(message, field_name)
    if isinstance(detail, list) or isinstance(detail, tuple):
        return get_first_error_message(detail[0])
    return None, str(detail)


def get_exception_message(exc):
    try:
        return get_first_error_message(exc.detail)
    except:
        return None, str(exc)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response:
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            field_name, message = get_exception_message(exc)
            response.data = {
                'detail': message,
                'error_field': field_name,
            }

        # un comment these two lines if you want to return 400 status code for not found objects (Wrong ID)
        # if response.status_code == status.HTTP_404_NOT_FOUND:
        #     response.status_code = status.HTTP_400_BAD_REQUEST

    return response
