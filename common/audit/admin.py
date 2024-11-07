from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin
from safedelete.admin import SafeDeleteAdmin


class FieldsGetterMixin:
    list_display_valid_types = (
        models.AutoField,
        models.BigAutoField,
        models.BooleanField,
        models.CharField,
        models.CommaSeparatedIntegerField,
        models.DateField,
        models.DateTimeField,
        models.DecimalField,
        models.DurationField,
        models.EmailField,
        models.FileField,
        models.FilePathField,
        models.FloatField,
        models.ForeignKey,
        models.ImageField,
        models.IntegerField,
        models.GenericIPAddressField,
        models.NullBooleanField,
        models.PositiveIntegerField,
        models.PositiveSmallIntegerField,
        models.SlugField,
        models.SmallIntegerField,
        models.TimeField,
        models.URLField,
        models.UUIDField,
    )
    
    list_filter_valid_types = (
        models.AutoField,
        models.BigAutoField,
        models.BooleanField,
        models.CommaSeparatedIntegerField,
        models.DateField,
        models.DateTimeField,
        models.DecimalField,
        models.DurationField,
        models.FloatField,
        models.IntegerField,
        models.GenericIPAddressField,
        models.NullBooleanField,
        models.PositiveIntegerField,
        models.PositiveSmallIntegerField,
        models.SmallIntegerField,
        models.TimeField,
    )
    
    search_fields_valid_types = (
        models.AutoField,
        models.BigAutoField,
        models.CharField,
        models.CommaSeparatedIntegerField,
        models.EmailField,
        models.GenericIPAddressField,
        models.NullBooleanField,
        models.PositiveIntegerField,
        models.SlugField,
        models.TextField,
        models.URLField,
        models.UUIDField,
    )

    WEIGHTS = {
        'id': -1,
        # here are all another fields with value 0
        'created_at': 1,
        'created_by': 2,
        'updated_at': 3,
        'updated_by': 4,
        'deleted': 5,
        'deleted_by_cascade': 6,
    }

    def sort_fields(self, fields):
        return sorted(fields, key=lambda x: self.WEIGHTS.get(x, 0))

    def get_fields_from_valid_types(self, attribute_name, need_sort):
        if not getattr(self, f'use_{attribute_name}_getter', True):
            return getattr(self, attribute_name)
        
        valid_types_name = f'{attribute_name}_valid_types'
        valid_types = getattr(self, valid_types_name, tuple())

        fields = (
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, valid_types)
        )

        if need_sort:
            fields = self.sort_fields(fields)

        return tuple(fields)

    def get_list_display(self, request):
        return self.get_fields_from_valid_types('list_display', True)

    def get_list_filter(self, request):
        return self.get_fields_from_valid_types('list_filter', True)

    def get_search_fields(self, request):
        return self.get_fields_from_valid_types('search_fields', False)
    
    ordering = ('-updated_at', )


class SafeDeleteMixin(SafeDeleteAdmin):
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
    
    def get_queryset(self, request):
        return self.model.all_objects.all()

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        list_display = (o for o in list_display if o != 'id')
        return ('highlight_deleted_field', *list_display)

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        list_filter = filter(lambda filter: bool(filter != self.DeletedFilter.parameter_name), list_filter)
        return (self.DeletedFilter, *list_filter)

    field_to_highlight = 'id'

SafeDeleteMixin.highlight_deleted_field.short_description = SafeDeleteMixin.field_to_highlight


class AuditModelAdmin(SafeDeleteMixin, FieldsGetterMixin, SimpleHistoryAdmin):
    pass
