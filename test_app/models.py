from django.db import models
from common.audit.models import AuditModel


class TestTranslationModel(models.Model):
    text = models.CharField(max_length=100)
    translated_text = models.JSONField()


class TestTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    timezone_now = models.DateTimeField()
    timezone_localtime_timezone_now = models.DateTimeField()


class TestDeleteModel(AuditModel):
    text = models.CharField(max_length=100)
    un = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['un'],
                condition=models.Q(deleted__isnull=True),
                name='unique_active_un',
            ),
        ]


class TestDeleteModel2(AuditModel):
    base = models.ForeignKey(TestDeleteModel, models.CASCADE, related_name="bases")
    text = models.CharField(max_length=100)
