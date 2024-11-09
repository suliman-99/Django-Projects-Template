from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(AuditModelAdmin):
    pass