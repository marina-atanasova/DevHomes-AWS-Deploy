from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from random import choices

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from Listings.choices import CityChoices, PropertyTypeChoices, BuildTypeChoices, HeatingTypeChoices, \
    AptExposureChoices, DistrictChoices, AmenityCategoryChoices


# Create your models here.


class Amenity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(
        max_length=30,
        choices=AmenityCategoryChoices.choices,
        default=AmenityCategoryChoices.COMFORT,
    )
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Property(models.Model):
    broker = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='broker_listings',
        limit_choices_to={'role': 'broker'},
    )

    name = models.CharField(max_length=150)
    address = models.CharField("Address", max_length=255)
    city = models.CharField(choices=CityChoices)
    district = models.CharField(choices=DistrictChoices)
    size = models.PositiveIntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    bedrooms = models.PositiveIntegerField(default=0)
    rooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    balconies = models.PositiveIntegerField(default=0)

    property_type = models.CharField(max_length=255,
        choices = PropertyTypeChoices.choices,
        default= PropertyTypeChoices.Other

    )
    build_year = models.PositiveIntegerField(default=0)
    build_type = models.CharField(max_length=255,
                                  choices=BuildTypeChoices.choices,
                                  default=BuildTypeChoices.Other
                                  )
    description = models.TextField(blank=True, null=True)
    heating = models.CharField(max_length=255,
                               choices=HeatingTypeChoices.choices,
                               default=HeatingTypeChoices.Other)
    exposure = ArrayField(
        base_field=models.CharField(max_length=1, choices=AptExposureChoices.choices),
        default=list,
        blank=True,
    )
    floor = models.CharField(max_length=255, default=0)

    amenities = models.ManyToManyField(Amenity, blank=True, related_name="properties")

    @property
    def price_per_sqm(self):
        try:
            price = Decimal(str(self.price))
            size = Decimal(str(self.size))
            if self.size <= 0:
                return None
            return (price / size).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )
        except (AttributeError, TypeError, ZeroDivisionError, InvalidOperation):
            return None

    def __str__(self):
        return self.name