from simple_history.admin import SimpleHistoryAdmin


class AuditModelAdmin(SimpleHistoryAdmin):
    def get_queryset(self, request):
        return self.model.all_objects.all()
