from safedelete.queryset import SafeDeleteQueryset
from common.signals.querysets import BulkSignalQuerySet


class SafeDeleteBulkSignalQuerySet(BulkSignalQuerySet, SafeDeleteQueryset):
    pass
