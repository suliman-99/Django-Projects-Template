from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(AuditModelAdmin):
    list_display = (
        'id',
        'title',
        'body',
        *audit_fields,
    )
    list_filter = (
        *audit_fields,
    )
    search_fields = (
        'title',
        'body',
    )
    ordering = (
        '-updated_at',
    )