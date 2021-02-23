from django.db import models
from django import forms
from .choices import ORDER_STATUS, ORDER_TYPES, FIAT_TYPES, CRYPTO_TYPES, EMAIL_STATUS, TELEGRAM_STATUS

class Kyc(models.Model):
    first_name      = models.CharField(max_length=250)
    last_name       = models.CharField(max_length=250)
    phone_number    = models.CharField(max_length=250)
    email_address   = models.CharField(max_length=250)
    password        = models.CharField(max_length=250, null=True, blank=True)
    nin_number      = models.CharField(max_length=250)
    id_front        = models.FileField(upload_to='kyc/', null=True, blank=True)
    id_back         = models.FileField(upload_to='kyc/', null=True, blank=True)
    selfie_photo    = models.FileField(upload_to='kyc/', null=True, blank=True)
    active          = models.BooleanField(default=False)
    activated_on    = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_submitted  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "Kyc for {} {} {}".format(self.first_name, self.last_name, self.email_address)

class AccountUser(models.Model):
    first_name          =   models.CharField(max_length=250)
    last_name           =   models.CharField(max_length=250)
    email_address       =   models.CharField(max_length=250)
    password            =   models.CharField(max_length=250, null=True, blank=True)
    role                =   models.IntegerField()
    active              =   models.BooleanField(default=False)
    account_status      =   models.IntegerField()
    date_added          =   models.DateTimeField(auto_now_add=True)

class PasswordResets(models.Model):
    related_account =   models.ForeignKey(Kyc, on_delete=models.CASCADE, related_name="reset_related_account")
    reset_token     =   models.CharField(max_length=250)
    reset_used      =   models.BooleanField(default=False)
    date_requested  =   models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    order_number                = models.CharField(max_length=250)
    related_kyc                 = models.ForeignKey(Kyc, on_delete=models.CASCADE, related_name="related_kyc")
    order_type                  = models.CharField(max_length=10, choices=ORDER_TYPES)
    wallet_address              = models.CharField(max_length=250, null=True, blank=True)     
    crypto_type                 = models.CharField(max_length=10, choices=CRYPTO_TYPES)  
    fiat_type                   = models.CharField(max_length=10, choices=FIAT_TYPES, default='UGX')  
    order_amount_crypto         = models.DecimalField(max_digits=20, decimal_places=15)
    order_amount_fiat           = models.DecimalField(max_digits=20, decimal_places=2)   
    crypto_address              = models.CharField(max_length=250, null=True, blank=True)
    crypto_fees                 = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    total_payable_amount_fiat   = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    warning                     = models.IntegerField(default=0)
    order_status                = models.CharField(max_length=15, choices=ORDER_STATUS, default='UNFULFILLED')  
    crypto_unit_price           = models.DecimalField(max_digits=20, decimal_places=2)
    completed_by                = models.CharField(max_length=250, null=True, blank=True)
    fullfilled_by               = models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name="order_fullfiller", null=True, blank=True)
    date_ordered                = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

class EmailLogs(models.Model):
    related_order_email = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_related_email")
    support_email       = models.CharField(max_length=250)
    client_email        = models.CharField(max_length=250)
    email_message       = models.TextField()
    status              = models.CharField(max_length=15, choices=EMAIL_STATUS, default='UNDELIVERED')
    date_dispatched     = models.DateTimeField(auto_now_add=True)

class TelegramLogs(models.Model):
    related_order_telegram = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="order_related_telegram")
    telegram_message       = models.TextField()
    status                 = models.CharField(max_length=15, choices=TELEGRAM_STATUS, default='UNDELIVERED')
    date_dispatched        = models.DateTimeField(auto_now_add=True)

class UserLogins(models.Model):
    related_user    =   models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name="user_logins")
    last_login      =   models.DateTimeField(auto_now_add=False, null=True, blank=True)
    last_token      =   models.CharField(max_length=250, null=True, blank=True)

class UserRefreshOtp(models.Model):
    related_user    =   models.ForeignKey(AccountUser, on_delete=models.CASCADE, related_name="user_refresh_otps")
    refresh_otp     =   models.CharField(max_length=5)
    token_status    =   models.BooleanField(default=True)
    token_expiry    =   models.DateTimeField(auto_now_add=False, null=True, blank=True)
    date_requested  =   models.DateTimeField(auto_now_add=True)