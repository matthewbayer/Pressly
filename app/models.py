from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    num_credits = models.IntegerField(default=10)
    email = models.EmailField(unique=True)
    email_confirmed = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False, verbose_name = "Admin approved for Beta use")
    username = None

    REQUIRED_FIELDS = ["password", "email_confirmed"]
    USERNAME_FIELD = "email"
    
    objects = CustomUserManager()

    class Meta:
        ordering = ['-num_credits']

    def __str__(self):
        return self.email

    def is_approved(self):
        return self.admin_approved

class NewsletterSubscription(models.Model):
    email = models.EmailField()
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.email

class PressReleaseSubmission(models.Model):
    # TODO: include text gen settings like temperature

    release_date = models.DateField(null=True)
    location = models.TextField(null=True)
    title = models.TextField(null=True)
    company_descriptions = models.TextField(null=True)
    details = models.TextField(null=True)
    generated_text = models.TextField(null=True)
    submission_date = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name="user who submitted")
    rating = models.BooleanField(null=True, verbose_name="whether or not the user gave the generation a thumbs up")
    REQUIRED_FIELDS = [
        "generated_text",
        "submission_date",
        "user",
        "release_date",
        "location",
        "title",
        "company_descriptions",
        "details"
    ]

    class Meta:
        ordering = ['-submission_date', "user"]


