from django.contrib.auth import get_user_model
from django.dispatch import receiver
from safedelete.signals import (
    pre_softdelete,
    post_softdelete,
    post_undelete,
)


User = get_user_model()


@receiver(pre_softdelete, sender=User, weak=False)
def handler(**kwargs):
    print('pre_softdelete')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_softdelete, sender=User, weak=False)
def handler(**kwargs):
    print('post_softdelete')
    print(kwargs)
    print('------------------------------------------')


@receiver(post_undelete, sender=User, weak=False)
def handler(**kwargs):
    print('post_undelete')
    print(kwargs)
    print('------------------------------------------')
