from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication
from common.headers import validate_and_coordinate_request_headers


class HeadersAuthentication(BaseAuthentication):
    def authenticate(self, request: Request):
        validate_and_coordinate_request_headers(request)
        return None
