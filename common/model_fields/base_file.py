from django.db import models


class CustomFileField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 500)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if kwargs.get('max_length') == 500:
            kwargs.pop('max_length')
        return name, path, args, kwargs
