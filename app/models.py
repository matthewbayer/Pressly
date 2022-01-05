from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    num_credits = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    username = None

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"
    
    objects = CustomUserManager()

    class Meta:
        ordering = ['-num_credits']

    def __str__(self):
        return self.email