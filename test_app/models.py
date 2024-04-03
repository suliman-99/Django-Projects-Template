from django.db import models
from common.audit.models import AuditModel, HistoricalAuditModel


class Test(AuditModel):
    text = models.CharField(max_length=100, null=False, blank=False)
    un = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['un'],
                condition=models.Q(deleted__isnull=True),
                name='unique_active_un',
            ),
        ]


class SubTest(HistoricalAuditModel):
    test = models.ForeignKey(Test, models.CASCADE, related_name="sub_tests")
    text = models.CharField(max_length=100)


class TestTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    timezone_now = models.DateTimeField()
    timezone_localtime_timezone_now = models.DateTimeField()
