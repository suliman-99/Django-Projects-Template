from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from .models import TestTimeModel, Test, SubTest


@admin.register(Test)
class TestAdmin(AuditModelAdmin):
    pass


@admin.register(SubTest)
class SubtestAdmin(AuditModelAdmin):
    pass


@admin.register(TestTimeModel)
class TestTimeModelAdmin(AuditModelAdmin):
    pass
