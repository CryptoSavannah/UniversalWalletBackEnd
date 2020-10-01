from django.contrib import admin

from .models import LoyaltyTenants, LoyaltyProgram, LoyaltyProgramSubscriptions, LoyaltyProgramTransactions

admin.site.register(LoyaltyTenants)
admin.site.register(LoyaltyProgramSubscriptions)
admin.site.register(LoyaltyProgram)
admin.site.register(LoyaltyProgramTransactions)