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
    date_submitted  = models.DateTimeField(auto_now_add=True)

class Orders(models.Model):
    order_number    = models.CharField(max_length=250)
    related_kyc     = models.ForeignKey(Kyc, on_delete=models.CASCADE, related_name="related_kyc")
    order_type      = models.CharField(max_length=10, choices=ORDER_TYPES)      
    crypto_type     = models.CharField(max_length=10, choices=CRYPTO_TYPES)  
    fiat_type       = models.CharField(max_length=10, choices=FIAT_TYPES, default='UGX')  
    order_amount_crypto  = models.DecimalField(max_digits=20, decimal_places=6)
    order_amount_fiat    = models.DecimalField(max_digits=20, decimal_places=2)   
    order_status    = models.CharField(max_length=15, choices=ORDER_STATUS, default='UNFULFILLED')  
    crypto_unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    completed_by    = models.CharField(max_length=250, null=True, blank=True)
    date_ordered    = models.DateTimeField(auto_now_add=True)

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