from rest_framework import versioning


class HeaderVersioning(versioning.BaseVersioning):
    """
    A versioning scheme that uses a header value.
    """

    def determine_version(self, request, *args, **kwargs):
        """
        Determine the version based on the request header.
        """
        return request.headers.get('version', 1)
