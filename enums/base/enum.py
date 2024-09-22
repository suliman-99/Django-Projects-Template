from enum import Enum, IntEnum


def to_normal_case(s):
    # Replace underscores with spaces and capitalize the first letter of each word
    return s.replace('_', ' ').title().strip()


class EnumExtension:
    @classmethod
    @property
    def choices(cls):
        return tuple((o.value, o.label) for o in cls)
    
    @classmethod
    @property
    def values(cls):
        return tuple(o.value for o in cls)
    
    @classmethod
    @property
    def labels(cls):
        return tuple(o.label for o in cls)
    
    @property
    def label(self):
        return to_normal_case(self.name)
    
    def __eq__(self, value: object) -> bool:
        return bool(self.value == value)

    def __hash__(self):
        return hash(self.value)


class BaseEnum(EnumExtension, Enum):
    pass


class BaseIntEnum(EnumExtension, IntEnum):
    pass
