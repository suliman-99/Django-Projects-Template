from django.contrib import admin
from translation.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'native_name', 
        'code', 
        'is_active', 
        'is_default',
    )
