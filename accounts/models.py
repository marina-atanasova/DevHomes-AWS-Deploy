from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from Listings.models import Property
from accounts.choices import MessageStatusChoices, RequestTypeChoices


# Create your models here.

phone_validator = RegexValidator(
    regex=r'^[0-9+/]{6,12}$',
    message="Phone number must be 6–12 characters and may contain digits, + or /."
)

class UserInquiry(models.Model):
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inquiries',
        limit_choices_to={'role': 'customer'},
    )
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(
        max_length=12,
        validators=[phone_validator],
    )
    email = models.EmailField(max_length=50)
    listing = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="inquiries",
    )
    request_type = models.CharField(
        choices=RequestTypeChoices.choices,
        default=RequestTypeChoices.OTHER
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        choices=MessageStatusChoices.choices,
        default=MessageStatusChoices.NEW,
    )
    reply_message = models.TextField(blank=True, null=True)
    replied_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)


    def __str__(self):
        return f"Credit request {self.created_at:%Y-%m-%d}"

