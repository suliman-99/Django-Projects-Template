from django.core.exceptions import ValidationError


class SingletonModel():
    def save(self, *args, **kwargs):
        instance = self.__class__.objects.filter().first()
        if instance and instance.id != self.id:
            for field in self._meta.fields:
                if field.name not in ('id', 'pk'):
                    setattr(instance, field.name, getattr(self, field.name))
            instance.save()
            return
        return super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        raise ValidationError(f"Cannot delete an instance of {self.__class__.__name__}.")
