from typing import Any
from django.db import models
from currency.methods import get_primary_currency_id


class CurrencyField(models.ForeignKey):
    def __init__(self, *args, **kwargs):
        kwargs['to'] = 'currency.Currency'
        kwargs.setdefault('on_delete', models.PROTECT)
        kwargs.setdefault('default', get_primary_currency_id)
        kwargs.setdefault('related_name', '+')
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['to']
        return name, path, args, kwargs
