from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler
from rest_framework import status


def message_coordinator(message, field_name):
    message = message.replace("_id", "").replace("_", " ") 
    if message.startswith("This") and field_name is not None and field_name != 'non_field_errors':
        message = message + f' ({field_name})'
    return message.capitalize()


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
    # change the DjangoValidationError to DRFValidationError while i am in API not in django admin
    if isinstance(exc, DjangoValidationError):
        try:
            exc = DRFValidationError(detail=exc.message_dict)
        except:
            exc = DRFValidationError(detail=exc.messages)

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
