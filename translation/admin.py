from django.contrib import admin
from translation.models import Translation, Language


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


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'content_type', 
        'object_id', 
        'field_name', 
        'language_code', 
        'value',
    )
