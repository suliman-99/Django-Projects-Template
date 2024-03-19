

TEMPLATE_FLAG = '_______#IS_TEMPLATE#_______'


def response_template(data, message, error_field, code):
    return {
        'code': code,
        'message': message,
        'error_field': error_field,
        'data': data,
        TEMPLATE_FLAG: True,
    }


def success_response(data, message='Success.', code=None):
    return response_template(data, message, None, code)


def fail_response(message='Fail.', error_field=None, code=None):
    return response_template(None, message, error_field, code)
