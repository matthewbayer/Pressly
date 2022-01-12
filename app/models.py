from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    num_credits = models.IntegerField(default=10)
    email = models.EmailField(unique=True)
    username = None

    REQUIRED_FIELDS = ["password"]
    USERNAME_FIELD = "email"
    
    objects = CustomUserManager()

    class Meta:
        ordering = ['-num_credits']

    def __str__(self):
        return self.email

class NewsletterSubscription(models.Model):
    email = models.EmailField()
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

class PressReleaseSubmission(models.Model):
    generated_text = models.TextField()
    submission_date = models.DateTimeField()
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name="user who submitted")
    rating = models.BooleanField()
    REQUIRED_FIELDS = ["generated_text", "submission_date", "user"]

    class Meta:
        ordering = ['-submission_date', "user"]


