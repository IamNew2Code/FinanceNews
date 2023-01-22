from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account

class AccountAdmin(UserAdmin):
    
    # list determines what is going to be displayed on the admin page
    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    
    # search fields determines how to search for the data listed below
    search_fields = ('email', 'username')

    # things that will be restricted to change
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldssets = ()
    
admin.site.register(Account, AccountAdmin)
