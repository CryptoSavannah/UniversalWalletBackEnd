from django.contrib import admin

from .models import Kyc, Orders, PasswordResets

admin.site.register(Kyc)
admin.site.register(Orders)
admin.site.register(PasswordResets)
