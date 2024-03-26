from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import User
from users.forms import CustomAuthenticationForm


admin.site.login_form = CustomAuthenticationForm
# admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'first_login',
        'last_login',
        'last_refresh',
        'is_admin',

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
    )
