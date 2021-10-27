from django.contrib import admin
from Profiles.models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class AccountAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin','is_staff', 'is_active', 'is_superuser', 'email_confirmed')
    search_fields = ('email',)
    readonly_fields=('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Profile, AccountAdmin)