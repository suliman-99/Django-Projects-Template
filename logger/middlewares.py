from logger.models import Log
from rest_framework.request import Request


def get_user_from_request(request):
    return request.user if request.user.is_authenticated else None


def get_request_type(request):
    for type, _ in Log.TYPE_CHOICES:
        if request.method.startswith(f'/{type}/'):
            return type
    return Log.TYPE_OTHERS


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        Log.objects.create(
            type=get_request_type(request),
            user=get_user_from_request(request),
            status_code=response.status_code,
            url=request.path,
            query_params=request.GET,
            request_headers=dict(request.headers),
            request_body=request.POST,
            response_headers=dict(response.headers),
            response_body=getattr(response, 'data', None),
        )
        return response
 