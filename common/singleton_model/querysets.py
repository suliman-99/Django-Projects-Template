from django.db import models


class SingletonQuerySet(models.QuerySet):
    def bulk_create(self, objs, *args, **kwargs):
        if len(objs) < 1:
            return []
        elif len(objs) > 1:
            raise ValueError(f'Cannot Create more than Single instance of {self.model}')
        return super().bulk_create(objs, *args, **kwargs)
        
    def delete(self, *args, **kwargs):
        raise ValueError(f'Cannot delete {self.model} Single instance')
