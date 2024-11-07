from django.http import JsonResponse
from django.conf import settings
from rest_framework.exceptions import NotAcceptable
from enums.enums import OsType, OsType

# -------------------------------------------------------------------------------------------------

def validation_decorator(name):
    def return_decorator(method):
        def decorated_method(value):
            if not value:
                if settings.RAISE_EXCEPTION_FOR_MISSED_HEADER:
                    raise NotAcceptable(f'{name} is required in the header.')
                return None
            try:
                return method(value)
            except ValueError:
                raise NotAcceptable(f'Invalid {name}.')
        return decorated_method
    return return_decorator

# -------------------------------------------------------------------------------------------------

@validation_decorator('os-type')
def validate_os_type(value: str) -> None:
    value = int(value) # delete this if the os-type is string not int
    if value not in OsType.values:
        raise ValueError()
    return value


@validation_decorator('app-version')
def validate_app_version(value: str) -> None:
    parts = value.split('.')
    if len(parts) > 4:
        raise ValueError()
    for part in parts:
        int(part)
    return value

# -------------------------------------------------------------------------------------------------

def validate_and_coordinate_request_headers(request):
    headers = request.headers
    request.os_type = validate_os_type(headers.get('os-type'))
    request.app_version = validate_app_version(headers.get('app-version'))
    
# -------------------------------------------------------------------------------------------------

class HeaderValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            try:
                validate_and_coordinate_request_headers(request)
            except BaseException as e:
                return JsonResponse({ 'detail': str(e) }, status=e.status_code)
        
        return self.get_response(request)
