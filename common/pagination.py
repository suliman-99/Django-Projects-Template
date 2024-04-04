import math
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


PAGINATION_FLAG = '__IS_PAGINATED_RESPONSE__'


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    # def get_page_number(self, request, paginator):
    #     self.page_number = super().get_page_number(request, paginator)
    #     return self.page_number

    def get_paginated_response(self, data):
        return Response({
            PAGINATION_FLAG: True,
            'pagination': {
                'count': self.page.paginator.count,
                'pages_count': math.ceil(self.page.paginator.count/self.page_size),
                # 'page_size': self.page_size,
                # 'page': self.page_number,
                # 'next': self.get_next_link(),
                # 'previous': self.get_previous_link(),
            },
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'pagination': {
                    'type': 'object',
                    'properties': {
                        'count': {
                            'type': 'integer',
                            'example': 123,
                        },
                        'pages_count': {
                            'type': 'integer',
                            'example': 123,
                        },
                    },
                },
                'results': schema,
            },
        }
