from django.db import models
from django.core import validators


class SVGField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', []).append(validators.FileExtensionValidator(['svg']))
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for validator in kwargs.get('validators', []):
            if isinstance(validator, validators.FileExtensionValidator) and len(validator.allowed_extensions) == 1 and validator.allowed_extensions[0] == 'svg':
                kwargs['validators'].remove(validator)
                break
        return name, path, args, kwargs

