from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Permission, Group
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from .models import User
from .forms import CustomAuthenticationForm
from .methods import get_permission_full_name


admin.site.login_form = CustomAuthenticationForm


@admin.register(User)
class UserAdmin(UserAdmin, AuditModelAdmin):
    fieldsets = None
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        'id',
        
        'is_active',
        'is_staff',
        'is_superuser',
        'is_admin',

        'date_joined',
        'first_login',
        'last_login',
        'last_refresh',

        'email',
        'email_code_time',
        'email_code_is_valid',
        'email_verified',

        'phone_number',
        'phone_number_verified',

        'reset_password_code_time',
        'reset_password_code_is_valid',

        'first_name',
        'last_name',
        'language_code',
        *audit_fields,
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_admin',

        'date_joined',
        'first_login',
        'last_login',
        'last_refresh',

        'email',
        'email_code_time',
        'email_code_is_valid',
        'email_verified',

        'phone_number',
        'phone_number_verified',

        'reset_password_code_time',
        'reset_password_code_is_valid',

        'first_name',
        'last_name',
        'language_code',
        *audit_fields,
    )
    search_fields = (
        'email',

        'phone_number',

        'first_name',
        'last_name',
        'language_code',
    )
    ordering = (
        '-updated_at',
    )
    

admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(GroupAdmin):
    list_display = (
        'id', 
        'name',
    )
    search_fields = (
        'id', 
        'name',
    )
    ordering = (
        'id', 
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'name', 
        'codename', 
        'full_name', 
        'content_type',
    )
    list_filter = (
        'content_type__app_label', 
        'content_type__model', 
        'content_type',
    )
    search_fields = (
        'name', 
        'codename', 
        'content_type__app_label', 
        'content_type__model',
    )
    ordering = (
        'id',
    )

    def full_name(self, obj):
        return get_permission_full_name(obj)
