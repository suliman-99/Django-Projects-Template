from django.db import models
from django.core import validators


class CustomDecimalField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 20
        kwargs['decimal_places'] = 6
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['max_digits']
        del kwargs['decimal_places']
        return name, path, args, kwargs


class PriceField(CustomDecimalField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs.setdefault('validators', []).append(validators.MinValueValidator(0))
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        for validator in kwargs.get('validators', []):
            if isinstance(validator, validators.MinValueValidator) and validator.limit_value == 0:
                kwargs['validators'].remove(validator)
                break
        return name, path, args, kwargs
