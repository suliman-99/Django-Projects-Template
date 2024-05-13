from django.db import models
from django.db.models.signals import (
    pre_save, 
    post_save, 
    pre_delete,
    post_delete,
)
from common.signals import (
    pre_bulk_create,
    post_bulk_create,
    pre_bulk_update,
    post_bulk_update,
    pre_bulk_delete,
    post_bulk_delete,
)


class BulkCreateSignalQuerySet(models.QuerySet):
    def bulk_create(self, objs: list, *args, **kwargs) -> list:
        for obj in objs:
            pre_save.send_robust(
                sender=self.model,
                instance=obj,
                created=True,
                update_fields=None,
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        pre_bulk_create.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
        )

        created_objs = super().bulk_create(objs, *args, **kwargs)

        post_bulk_create.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
        )

        for obj in created_objs:
            post_save.send_robust(
                sender=self.model,
                instance=obj,
                created=True,
                update_fields=None,
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        return created_objs


class BulkUpdateSignalQuerySet(models.QuerySet):
    def bulk_update(self, objs: list, *args, **kwargs) -> int:
        for obj in objs:
            pre_save.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=kwargs.get('update_fields'),
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        pre_bulk_update.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
            update_fields=kwargs.get('update_fields'),
        )

        ret = super().bulk_update(objs, *args, **kwargs)

        post_bulk_update.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
            update_fields=kwargs.get('update_fields'),
        )

        for obj in objs:
            post_save.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=kwargs.get('update_fields'),
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        return ret
    
    def update(self, **kwargs) -> int:

        objs = list(self.all())
        for obj in objs:
            for key, value in kwargs.items():
                setattr(obj, key, value)

        update_fields = list(kwargs.keys())
        
        for obj in objs:
            pre_save.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=update_fields,
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        pre_bulk_update.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
            update_fields=update_fields,
            data=kwargs,
        )

        ret = super().update(**kwargs)

        post_bulk_update.send_robust(
            sender=self.model,
            using=kwargs.get('using'),
            queryset=self,
            update_fields=update_fields,
            data=kwargs,
        )

        for obj in objs:
            post_save.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=update_fields,
                raw=False,
                using=kwargs.get('using'),
                is_bulk=True,
            )

        return ret


class BulkDeleteSignalQuerySet(models.QuerySet):
    def delete(self) -> tuple[int, dict[str, int]]:
        objs = list(self.all())
        
        for obj in objs:
            pre_delete.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=None,
                raw=False,
                is_bulk=True,
            )

        pre_bulk_delete.send_robust(
            sender=self.model,
            queryset=self,
        )

        ret = super().delete()

        post_bulk_delete.send_robust(
            sender=self.model,
            queryset=self,
        )

        for obj in objs:
            post_delete.send_robust(
                sender=self.model,
                instance=obj,
                created=False,
                update_fields=None,
                raw=False,
                is_bulk=True,
            )
        
        return ret


class BulkSignalQuerySet(
    BulkCreateSignalQuerySet,
    BulkUpdateSignalQuerySet,
    BulkDeleteSignalQuerySet
):
    pass
