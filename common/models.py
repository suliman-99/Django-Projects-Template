from django.db import models
from django.core.validators import FileExtensionValidator


class SVGField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', []).append(FileExtensionValidator(['svg']))
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["validators"]
        return name, path, args, kwargs


class CustomDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 20
        kwargs['decimal_places'] = 6
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["max_digits"]
        del kwargs["decimal_places"]
        return name, path, args, kwargs
