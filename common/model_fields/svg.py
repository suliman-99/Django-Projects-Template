from django.core import validators
from .base_file import CustomFileField
from .added_validators import AddedValidatorsPlug


class SVGField(AddedValidatorsPlug, CustomFileField):
    added_validators = (validators.FileExtensionValidator(['svg']), )
