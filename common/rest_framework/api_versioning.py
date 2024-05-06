from rest_framework import versioning


class CustomURLPathVersioning(versioning.URLPathVersioning):
    default_version = 1
    version_param = 'version'
