from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, 
    pre_save, 
    post_delete, 
    pre_delete,
)


User = get_user_model()


@receiver(pre_save, sender=User, weak=False)
def handler(**kwargs):
    print('pre_save')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_save, sender=User, weak=False)
def handler(**kwargs):
    print('post_save')
    print(kwargs)
    print('------------------------------------------')


@receiver(pre_delete, sender=User, weak=False)
def handler(**kwargs):
    print('pre_delete')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_delete, sender=User, weak=False)
def handler(**kwargs):
    print('post_delete')
    print(kwargs)
    print('------------------------------------------')
