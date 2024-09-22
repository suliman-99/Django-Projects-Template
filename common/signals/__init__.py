from django.db.models.signals import ModelSignal


pre_bulk_create = ModelSignal(use_caching=True)
post_bulk_create = ModelSignal(use_caching=True)

pre_bulk_update = ModelSignal(use_caching=True)
post_bulk_update = ModelSignal(use_caching=True)

pre_bulk_delete = ModelSignal(use_caching=True)
post_bulk_delete = ModelSignal(use_caching=True)
