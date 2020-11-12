from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import COUNTRIES

# Create your models here.
class User(AbstractUser):
    prefix              =   models.CharField(max_length=4, choices=COUNTRIES, null=True, blank=True)
    location            =   models.CharField(max_length=250)
    active              =   models.BooleanField(default=False)
    date_added          =   models.DateTimeField(auto_now_add=True)

class Otp(models.Model):
    user            =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_otp")
    otp_code        =   models.CharField(max_length=4)
    dispatched      =   models.BooleanField(default=False)
    used            =   models.BooleanField(default=False)
    date_created    =   models.DateTimeField(auto_now_add=True)

