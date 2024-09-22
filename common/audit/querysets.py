from safedelete.queryset import SafeDeleteQueryset
from ..signals.querysets import BulkSignalQuerySet


class SafeDeleteBulkSignalQuerySet(BulkSignalQuerySet, SafeDeleteQueryset):
    pass
