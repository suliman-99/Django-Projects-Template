from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


@admin.register(ContentType)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'app_label', 
        'model',
    )
    list_filter = (
        'app_label', 
        'model',
    )
    search_fields = (
        'id', 
        'app_label', 
        'model',
    )
    ordering = (
        'id',
    )
