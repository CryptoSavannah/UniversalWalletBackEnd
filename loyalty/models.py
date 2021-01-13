from django.db import models
from accounts.models import User

class Partnerships(models.Model):
    partner_name    = models.CharField(max_length=250)
    partner_product = models.CharField(max_length=250)
    partner_contact = models.CharField(max_length=250)
    percentage_points = models.DecimalField(max_digits=20, decimal_places=2)
    partner_returns   = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    status            = models.BooleanField(default=True)
    date_added        = models.DateTimeField(auto_now_add=True)

class LoyaltyTenants(models.Model):
    tenant_name            =    models.CharField(max_length=250)
    related_user_account   =    models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_related_account")
    tenant_description     =    models.CharField(max_length=250)
    tenant_contact         =    models.CharField(max_length=250)
    status                 =    models.BooleanField(default=True)
    date_added             =    models.DateTimeField(auto_now_add=True)

class LoyaltyProgram(models.Model):
    program_name        = models.CharField(max_length=250)
    products_attached   = models.CharField(max_length=250)
    related_tenant      = models.ForeignKey(LoyaltyTenants, on_delete=models.CASCADE, related_name="related_tenant", blank=True, null=True)
    program_partner     = models.ForeignKey(Partnerships, on_delete=models.CASCADE, related_name="program_partner", blank=True, null=True)
    program_percentage  = models.DecimalField(max_digits=20, decimal_places=2)
    partner_percentage  = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    balance             = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    start_date          = models.DateField(auto_now_add=False, blank=True, null=True)
    due_date            = models.DateField(auto_now_add=False, blank=True, null=True)
    status              = models.BooleanField(default=True)
    date_added          = models.DateTimeField(auto_now_add=True)

class LoyaltyProgramBranches(models.Model):
    related_loyalty_program = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="branch_related_loyalty_program")
    branch_name             =  models.CharField(max_length=250)
    branch_location         =  models.CharField(max_length=250)
    status                  =  models.BooleanField(default=True)
    date_added              =  models.DateTimeField(auto_now_add=True)

class LoyaltyProgramBalanceLoads(models.Model):
    related_loyalty_program =  models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="balance_related_loyalty_program")
    amount                  =  models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    status                  =  models.BooleanField(default=False)
    date_loaded             =  models.DateTimeField(auto_now_add=True)


class LoyaltyProgramSubscriptions(models.Model):
    related_loyalty_program =   models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="program_related")
    related_user            =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_user")
    status                  =   models.BooleanField(default=True)
    card_number             =   models.CharField(max_length=250)
    points_earned           =   models.DecimalField(max_digits=20, decimal_places=2, default=0)
    rating                  =   models.DecimalField(max_digits=20, decimal_places=2, default=0)
    date_suspended          =   models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_unsubscribed       =   models.DateTimeField(auto_now_add=False, blank=True, null=True)
    date_subscribed         =   models.DateTimeField(auto_now_add=True)

class LoyaltyUserPoints(models.Model):
    related_subscription  = models.ForeignKey(LoyaltyProgramSubscriptions, on_delete=models.CASCADE, related_name="user_loyalty_subscriptions", null=True, blank=True)
    points_accrued        = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    rating                = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    active                = models.BooleanField(default=True)
    date_added            = models.DateTimeField(auto_now_add=True)

class LoyaltyProgramTransactions(models.Model):
    related_program     = models.ForeignKey(LoyaltyProgram, on_delete=models.CASCADE, related_name="program_related_transactions")
    related_user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="points_user")
    related_branch      = models.ForeignKey(LoyaltyProgramBranches, on_delete=models.CASCADE, related_name="branch_transactions", null=True, blank=True)
    transaction_amount  = models.DecimalField(max_digits=20, decimal_places=2)
    receipt_number      = models.CharField(max_length=250)
    points_awarded      = models.DecimalField(max_digits=20, decimal_places=2)
    payment_mode        = models.CharField(max_length=250, default="CASH")
    transaction_date    = models.DateField(auto_now_add=False, blank=True, null=True)
    date_added          = models.DateTimeField(auto_now_add=True)