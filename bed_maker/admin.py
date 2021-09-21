from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(BedfileRequest)
admin.site.register(Gene)
admin.site.register(Transcript)

class AccountAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email','date_joined', 'last_login', 'is_admin','is_staff', 'is_active', 'is_superuser', 'email_confirmed')
    search_fields = ('email',)
    readonly_fields=('id', 'date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Profile, AccountAdmin)