from django.contrib import admin

from .models import Kyc, Orders, PasswordResets, AccountUser

admin.site.register(Kyc)
admin.site.register(Orders)
admin.site.register(PasswordResets)
admin.site.register(AccountUser)