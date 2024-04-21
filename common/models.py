from django.db import models
from django.core.validators import FileExtensionValidator


class SVGField(models.FileField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault('validators', []).append(FileExtensionValidator(['svg']))
        super().__init__(*args, **kwargs)


class CustomDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs['max_digits'] = 20
        kwargs['decimal_places'] = 6
        super().__init__(*args, **kwargs)
