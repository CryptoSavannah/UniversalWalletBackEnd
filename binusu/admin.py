from django.contrib import admin

from .models import Kyc, Orders, PasswordResets, AccountUser, OrderCompletions

admin.site.register(Kyc)
admin.site.register(Orders)
admin.site.register(PasswordResets)
admin.site.register(AccountUser)
admin.site.register(OrderCompletions)