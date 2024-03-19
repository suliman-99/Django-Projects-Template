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
        'email',
        'email_code_is_valid',
        'phone_number',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
