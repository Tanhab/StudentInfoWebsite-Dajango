from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin


# Register your models here.

# custom design for Admin panel
class AccountAdmin(UserAdmin):
    # what you want to show in admin panel for users
    list_display = ('reg_num', 'username', 'date_joined', 'last_login', 'address', 'phone_number','blood_group')

    # search parameters
    search_fields = ('reg_num', 'username',)
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)
