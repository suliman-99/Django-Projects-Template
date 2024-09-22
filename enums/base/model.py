from django.db import models
from common.model_fields.name import NameField


class EnumModel(models.Model):
    name = NameField(primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
