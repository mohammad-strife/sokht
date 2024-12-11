from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class CustomUser(AbstractUser):
    n_code = models.IntegerField(default=0000000000)
    phone = models.CharField(max_length=50,null=True,blank=True)
