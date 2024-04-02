from django.contrib import admin
from common.audit.admin import AuditModelAdmin
from common.audit.variables import audit_fields
from users.models import User
from users.forms import CustomAuthenticationForm


admin.site.login_form = CustomAuthenticationForm


@admin.register(User)
class UserAdmin(AuditModelAdmin):
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
