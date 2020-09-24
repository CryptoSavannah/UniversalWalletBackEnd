from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_number        =   models.CharField(max_length=12)
    pin_code            =   models.CharField(max_length=12, blank=True, null=True)
    location            =   models.CharField(max_length=250)
    active              =   models.BooleanField(default=True)
    date_added          =   models.DateTimeField(auto_now_add=True)

