from collections.abc import Sequence
from django.http import HttpRequest
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin


class DeletedFilter(admin.SimpleListFilter):
    title = _('deleted')
    parameter_name = 'deleted'

    def lookups(self, request, model_admin):
        return (
            ('not_deleted', _('Not Deleted')),
            ('deleted', _('Deleted')),
            ('both', _('Both')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value or value == 'not_deleted':
            return queryset.filter(deleted__isnull=True)
        elif value == 'deleted':
            return queryset.exclude(deleted__isnull=True)
        elif value == 'all':
            return queryset


class AuditModelAdmin(SimpleHistoryAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.all()

    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        list_filter = super().get_list_filter(request)
        list_filter = filter(lambda filter: bool(filter != 'deleted'), list_filter)
        return (DeletedFilter, *list_filter)
