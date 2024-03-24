from logging import Handler


class DataBaseHandler(Handler):
    def __init__(self, *args, level: int | str = 0, **kwargs) -> None:
        super().__init__(level)
    
    def emit(self, record):
        from logger.models import Log
        from logger.methods import get_request_type, get_user_from_request, get_html_message
        
        request = getattr(record, 'request', None)
        if request:
            Log.objects.create(
                level=record.levelname,
                type=get_request_type(request),
                user=get_user_from_request(request),
                method=request.method,
                url=request.path,
                message=record.message,
                html_message=get_html_message(record),
                query_params=request.GET,
                request_headers=dict(request.headers),
            )
