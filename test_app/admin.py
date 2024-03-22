from django.contrib import admin
from test_app.models import TestTranslationModel, TestTimeModel


@admin.register(TestTranslationModel)
class TestTranslationModelAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'translated_text',
    )


@admin.register(TestTimeModel)
class TestTimeModelAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 
        'timezone_now', 
        'timezone_localtime_timezone_now',
    )
