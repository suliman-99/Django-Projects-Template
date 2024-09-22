
_ISNULL = 'isnull'
_IN = 'in'
_EXACT = 'exact'

_IEXACT = 'iexact'
_CONTAINS = 'contains'
_ICONTAINS = 'icontains'
_STARTSWITH = 'startswith'
_ISTARTSWITH = 'istartswith'
_ENDSWITH = 'endswith'
_IENDSWITH = 'iendswith'
_REGEX = 'regex'
_IREGEX = 'iregex'

_LT = 'lt'
_LTE = 'lte'
_GT = 'gt'
_GTE = 'gte'
_RANGE = 'range'

_DATE = 'date'
_YEAR = 'year'
_ISO_YEAR = 'iso_year'
_MONTH = 'month'
_DAY = 'day'
_WEEK = 'week'
_WEEK_DAY = 'week_day'
_ISO_WEEK_DAY = 'iso_week_day'
_QUARTER = 'quarter'
_TIME = 'time'
_HOUR = 'hour'
_MINUTE = 'minute'
_SECOND = 'second'

_BASE_LOOKUPS= (
    _ISNULL, 
    _IN, 
    _EXACT,
)
_COMPARISON_LOOKUPS = (
    _LT, 
    _LTE, 
    _GT, 
    _GTE, 
    _RANGE,
)
_CHAR_LOOKUPS = (
    _IEXACT, 
    _CONTAINS, 
    _ICONTAINS, 
    _STARTSWITH, 
    _ISTARTSWITH, 
    _ENDSWITH, 
    _IENDSWITH, 
    _REGEX, 
    _IREGEX,
)
_DATE_LOOKUPS = (
    _YEAR, 
    _ISO_YEAR, 
    _MONTH, 
    _DAY, 
    _WEEK,
    _WEEK_DAY,
    _ISO_WEEK_DAY, 
    _QUARTER,
)
_TIME_LOOKUPS = (
    _HOUR, 
    _MINUTE, 
    _SECOND,
)
_DATETIME_LOOKUPS = (
    _DATE,
    _TIME,
)

_DATE_COMPARISON_LOOKUPS = [
    F'{_DATE_LOOKUP}__{_COMPARISON_LOOKUP}' 
    for _DATE_LOOKUP in _DATE_LOOKUPS 
    for _COMPARISON_LOOKUP in _COMPARISON_LOOKUPS
]
_TIME_COMPARISON_LOOKUPS = [
    F'{_TIME_LOOKUP}__{_COMPARISON_LOOKUP}' 
    for _TIME_LOOKUP in _TIME_LOOKUPS 
    for _COMPARISON_LOOKUP in _COMPARISON_LOOKUPS
]
_DATETIME_COMPARISON_LOOKUPS = [
    F'{_DATETIME_LOOKUP}__{_COMPARISON_LOOKUP}' 
    for _DATETIME_LOOKUP in _DATETIME_LOOKUPS 
    for _COMPARISON_LOOKUP in _COMPARISON_LOOKUPS
]

class FilterLookupExpr:
    OTHER = _BASE_LOOKUPS
    BOOLEAN = _BASE_LOOKUPS
    NUMBER = (
        *_BASE_LOOKUPS, 
        *_COMPARISON_LOOKUPS,
    )
    DATE = (
        *_BASE_LOOKUPS, 
        *_COMPARISON_LOOKUPS, 
        *_DATE_LOOKUPS, 
        *_DATE_COMPARISON_LOOKUPS,
    )
    TIME = (
        *_BASE_LOOKUPS, 
        *_COMPARISON_LOOKUPS, 
        *_TIME_LOOKUPS, 
        *_TIME_COMPARISON_LOOKUPS,
    )
    DATETIME = (
        *_BASE_LOOKUPS, 
        *_COMPARISON_LOOKUPS, 
        *_DATETIME_LOOKUPS, 
        *_DATETIME_COMPARISON_LOOKUPS, 
        *_DATE_LOOKUPS, 
        *_DATE_COMPARISON_LOOKUPS, 
        *_TIME_LOOKUPS, 
        *_TIME_COMPARISON_LOOKUPS,
    )
    DURATION = (
        *_BASE_LOOKUPS, 
        *_COMPARISON_LOOKUPS,
    )
    STRING = (
        *_BASE_LOOKUPS, 
        *_CHAR_LOOKUPS,
    )
