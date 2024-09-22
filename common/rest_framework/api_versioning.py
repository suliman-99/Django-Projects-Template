from rest_framework import versioning


class CustomURLPathVersioning(versioning.URLPathVersioning):
    default_version = 1
    version_param = 'version'


VERSION = r'v(?P<version>\d+)/'
OPTIONAL_VERSION = r'(v(?P<version>\d+)/)?'
