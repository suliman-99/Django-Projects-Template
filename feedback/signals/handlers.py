from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from notification.methods import default_translated_push_notifications
from ..models import Feedback


User = get_user_model()
    

@receiver(post_save, sender=Feedback, weak=False)
def feedback_handler(**kwargs):
    # feedback:Feedback = kwargs['instance']
    admins = list(User.objects.filter(is_admin=True))
    default_translated_push_notifications(
        users=admins,
        save=True,
        data={
            'title_ar': 'مراجعة',
            'title_en': 'Feedback',
            'body_ar': 'هناك مراجعة جديدة',
            'body_en': 'There is a new feedback.',
        }
    )
