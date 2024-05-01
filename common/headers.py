from django.conf import settings
from rest_framework.exceptions import NotAcceptable

# -------------------------------------------------------------------------------------------------

OS_TYPE_ANDROID = 1
OS_TYPE_IOS = 2
OS_TYPE_WEB = 3
OS_TYPE_WINDOWS = 4
OS_TYPE_LINUX = 5
OS_TYPE_MAC = 6

OS_TYPE_CHOICES = (
    (OS_TYPE_ANDROID, "Android"),
    (OS_TYPE_IOS, "IOS"),
    (OS_TYPE_WEB, "Web"),
    (OS_TYPE_WINDOWS, "Windows"),
    (OS_TYPE_LINUX, "Linux"),
    (OS_TYPE_MAC, "Mac"),
)

OS_TYPE_VALUES = [t[0] for t in OS_TYPE_CHOICES]
OS_TYPE_NAMES = [t[1] for t in OS_TYPE_CHOICES]

# -------------------------------------------------------------------------------------------------

APP_TYPE_ADMIN = 1
APP_TYPE_USER = 2

APP_TYPE_CHOICES = (
    (APP_TYPE_ADMIN, "Admin"),
    (APP_TYPE_USER, "User"),
)

APP_TYPE_VALUES = [t[0] for t in APP_TYPE_CHOICES]
APP_TYPE_NAMES = [t[1] for t in APP_TYPE_CHOICES]

# -------------------------------------------------------------------------------------------------

def validation_decorator(name):
    def return_decorator(method):
        def decorated_method(value):
            if not value:
                if settings.DEBUG:
                    return None
                raise NotAcceptable(f'{name} is required in the header.')
            try:
                return method(value)
            except ValueError:
                raise NotAcceptable(f'Invalid {name}.')
        return decorated_method
    return return_decorator

# -------------------------------------------------------------------------------------------------

@validation_decorator('os-type')
def validate_os_type(value: str) -> None:
    value = int(value)
    if value not in OS_TYPE_VALUES:
        raise ValueError()
    return value


@validation_decorator('app-type')
def validate_app_type(value: str) -> None:
    value = int(value)
    if value not in APP_TYPE_VALUES:
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
    request.app_type = validate_app_type(headers.get('app-type'))
    request.app_version = validate_app_version(headers.get('app-version'))
    
# -------------------------------------------------------------------------------------------------
