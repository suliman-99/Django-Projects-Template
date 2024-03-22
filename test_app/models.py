from django.db import models


class TestTranslationModel(models.Model):
    text = models.CharField(max_length=100)
    translated_text = models.CharField(max_length=100)


class TestTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    timezone_now = models.DateTimeField()
    timezone_localtime_timezone_now = models.DateTimeField()
