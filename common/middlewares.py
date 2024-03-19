import json
from rest_framework.response import Response
from common.pagination import PAGINATION_FLAG
from common.response_templates import TEMPLATE_FLAG, success_response, fail_response


class ResponseCoordinatorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response:Response = self.get_response(request)
        if not request.path.startswith('/api/') or not response.headers.get('Content-Type') == 'application/json':
            return response
        
        response_data = json.loads(response.content)

        if not TEMPLATE_FLAG in response_data:
            if 200 <= response.status_code < 300:
                if response_data.pop(PAGINATION_FLAG, None):
                    new_response_data = success_response({})
                    new_response_data.update(response_data)
                    
                    # This line just to make the data as lower as possible in the response
                    # Deleting This line will not effect any thing
                    new_response_data['data'] = new_response_data.pop('data') 
                    
                    response_data = new_response_data
                else:
                    response_data = success_response(response_data)

            else:
                response_data = fail_response(
                    message=response_data['detail'], 
                    error_field=response_data.get('error_field'),
                )

        response_data.pop(TEMPLATE_FLAG)
        response.content = json.dumps(response_data)
        return response
