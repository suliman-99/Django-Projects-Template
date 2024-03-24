from django.conf import settings
from django.utils.module_loading import import_string


def get_user_from_request(request):
    return request.user if request.user.is_authenticated else None


def get_request_type(request):
    return request.path.split('/')[1]


def get_html_message(record):
    request = getattr(record, 'request', None)
    reporter_class = import_string(settings.DEFAULT_EXCEPTION_REPORTER)
    if record.exc_info:
        exc_info = record.exc_info
    else:
        exc_info = (None, record.getMessage(), None)
    reporter = reporter_class(request, is_email=True, *exc_info)
    html_message = reporter.get_traceback_html()
    return html_message
