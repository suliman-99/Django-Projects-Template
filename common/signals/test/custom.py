from django.contrib.auth import get_user_model
from django.dispatch import receiver
from common.signals import (
    pre_bulk_create,
    post_bulk_create,
    pre_bulk_update,
    post_bulk_update,
    pre_bulk_delete,
    post_bulk_delete,
)


User = get_user_model()


@receiver(pre_bulk_create, sender=User, weak=False)
def handler(**kwargs):
    print('pre_bulk_create')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_bulk_create, sender=User, weak=False)
def handler(**kwargs):
    print('post_bulk_create')
    print(kwargs)
    print('------------------------------------------')


@receiver(pre_bulk_update, sender=User, weak=False)
def handler(**kwargs):
    print('pre_bulk_update')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_bulk_update, sender=User, weak=False)
def handler(**kwargs):
    print('post_bulk_update')
    print(kwargs)
    print('------------------------------------------')


@receiver(pre_bulk_delete, sender=User, weak=False)
def handler(**kwargs):
    print('pre_bulk_delete')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_bulk_delete, sender=User, weak=False)
def handler(**kwargs):
    print('post_bulk_delete')
    print(kwargs)
    print('------------------------------------------')
