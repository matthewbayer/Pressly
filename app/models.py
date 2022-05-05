from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager, SubmissionManager

import uuid

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

class StatusChoices(models.TextChoices):
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"

class PressReleaseSubmission(models.Model):
    # TODO: include text gen settings like temperature
    submission_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission_status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.PENDING, max_length=255)
    error_msg = models.TextField(null=True)
    iot = models.TextField(null=True)
    generated_text = models.TextField(null=True)
    submission_date = models.DateTimeField(null=True)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, verbose_name="user who submitted")
    REQUIRED_FIELDS = [
        "generated_text",
        "submission_date",
        "user",
        "iot"
    ]

    objects = SubmissionManager()

    class Meta:
        ordering = ['-submission_date', "user"]

    def set_complete(self):
        self.submission_status = StatusChoices.COMPLETE
        self.save()

    def set_error(self):
        self.submission_status = StatusChoices.ERROR
        self.save()

    def is_complete(self):
        return self.submission_status == StatusChoices.COMPLETE

    def is_pending(self):
        return self.submission_status == StatusChoices.PENDING

    def is_error(self):
        return self.submission_status == StatusChoices.ERROR


