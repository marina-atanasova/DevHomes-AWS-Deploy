from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r'^[0-9+/]{6,12}$',
    message="Phone number must be 6–12 characters and may contain digits, + or /.")


class UserRole(models.TextChoices):
    BROKER = 'broker', 'Broker'
    CUSTOMER = 'customer', 'Customer'


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(
        max_length=15,
        blank=True,
        validators=[phone_validator],
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.BROKER,
    )
    favorite_properties = models.ManyToManyField(
        'Listings.Property',
        blank=True,
        related_name='favorited_by',
    )

    def is_broker(self):
        return self.role == UserRole.BROKER

    def is_customer(self):
        return self.role == UserRole.CUSTOMER

    def __str__(self):
        return self.username