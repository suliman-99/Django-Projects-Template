import math
from rest_framework import pagination
from rest_framework.response import Response


PAGINATION_FLAG = '__IS_PAGINATED_RESPONSE__'


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    max_page_size = 1000
    page_size_query_param = 'page_size'

    def get_page_number(self, request, paginator):
        self.page_number = super().get_page_number(request, paginator)
        return self.page_number

    def get_paginated_response(self, data):
        return Response({
            PAGINATION_FLAG: True,
            'pagination': {
                'count': self.page.paginator.count,
                'pages_count': math.ceil(self.page.paginator.count/self.page_size),
                'page_size': self.page_size,
                'page': self.page_number,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'required': [
                'pagination', 
                'results',
            ],
            'properties': {
                'pagination': {
                    'type': 'object',
                    'required': [
                        'count', 
                        'pages_count', 
                        'page_size', 
                        'page', 
                        'next', 
                        'previous',
                    ],
                    'properties': {
                        'count': {
                            'type': 'integer',
                            'example': 1000,
                        },
                        'pages_count': {
                            'type': 'integer',
                            'example': 100,
                        },
                        'page_size': {
                            'type': 'integer',
                            'example': 10,
                        },
                        'page': {
                            'type': 'integer',
                            'example': 1,
                        },
                        'next': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': 'http://api.example.org/accounts/?{page_query_param}=4'.format(
                                page_query_param=self.page_query_param)
                        },
                        'previous': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': 'http://api.example.org/accounts/?{page_query_param}=2'.format(
                                page_query_param=self.page_query_param)
                        },
                    },
                },
                'results': schema,
            },
        }


class CustomLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000
    limit_query_param = 'pagination_limit'
    offset_query_param = 'pagination_offset'

    def get_paginated_response(self, data):
        return Response({
            PAGINATION_FLAG: True,
            'pagination': {
                'count': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data,
        })

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'required': [
                'pagination', 
                'results',
            ],
            'properties': {
                'pagination': {
                    'type': 'object',
                    'required': [
                        'count', 
                        'next', 
                        'previous',
                    ],
                    'properties': {
                        'count': {
                            'type': 'integer',
                            'example': 1000,
                        },
                        'next': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': 'http://api.example.org/accounts/?{offset_param}=400&{limit_param}=100'.format(
                                offset_param=self.offset_query_param, limit_param=self.limit_query_param),
                        },
                        'previous': {
                            'type': 'string',
                            'nullable': True,
                            'format': 'uri',
                            'example': 'http://api.example.org/accounts/?{offset_param}=200&{limit_param}=100'.format(
                                offset_param=self.offset_query_param, limit_param=self.limit_query_param),
                        },
                    }
                },
                'results': schema,
            },
        }
