from enum import EnumMeta, Enum, IntEnum


class EnumExtensionMeta(EnumMeta):
    def __getattribute__(self, name):
        ret = super().__getattribute__(name)
        if isinstance(ret, IntEnum):
            ret = int(ret)
        if isinstance(ret, Enum):
            ret = ret.value
        return ret


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


class BaseEnum(EnumExtension, Enum, metaclass=EnumExtensionMeta):
    pass


class BaseIntEnum(EnumExtension, IntEnum, metaclass=EnumExtensionMeta):
    pass
