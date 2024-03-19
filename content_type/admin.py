from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


@admin.register(ContentType)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'app_label', 'model')
