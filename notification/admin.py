from django.contrib import admin
from notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',

        'title',
        'body',
        'image',

        'user',
        'is_viewed',

        'created_at',
    )
