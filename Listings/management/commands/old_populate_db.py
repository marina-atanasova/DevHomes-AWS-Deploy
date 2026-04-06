import random

from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import Property, Amenity
from Listings.choices import (
    CityChoices,
    DistrictChoices,
    PropertyTypeChoices,
    BuildTypeChoices,
    HeatingTypeChoices,
    AptExposureChoices,
)


class Command(BaseCommand):
    help = "Populate the database with sample properties."

    @transaction.atomic
    def handle(self, *args, **options):
        Property.objects.all().delete()

        amenities = list(Amenity.objects.all())

        sample_addresses = [
            "12 Ivan Vazov St.",
            "88 Vitosha Blvd.",
            "4 Shipka St.",
            "112 Bulgaria Blvd.",
            "23 Oborishte St.",
            "7 Slivnitsa Blvd.",
            "51 Cherni Vrah Blvd.",
            "99 Rakovski St.",
        ]

        city_district_pairs = [
            (CityChoices.SOFIA, DistrictChoices.CENTER),
            (CityChoices.SOFIA, DistrictChoices.LOZENETS),
            (CityChoices.SOFIA, DistrictChoices.MLADOST),
            (CityChoices.PLOVDIV, DistrictChoices.TRAKIA),
            (CityChoices.VARNA, DistrictChoices.CHAYKA),
            (CityChoices.BURGAS, DistrictChoices.LAZUR),
            (CityChoices.RUSE, DistrictChoices.ZDRAVETS),
        ]

        adjectives = ["Sunny", "Cozy", "Spacious", "Modern", "Bright", "Renovated"]
        created = 0

        for i in range(12):
            city, district = random.choice(city_district_pairs)
            bedrooms = random.choice([1, 2, 3])
            rooms = max(bedrooms + 1, random.choice([2, 3, 4, 5]))
            size = random.choice([45, 60, 75, 90, 110, 140])
            price = random.choice([85000, 120000, 165000, 220000, 350000])
            exposure_count = random.choice([1, 2])
            exposure = random.sample(
                [choice[0] for choice in AptExposureChoices.choices],
                k=exposure_count,
            )

            prop = Property.objects.create(
                name=f"{random.choice(adjectives)} {bedrooms}-bedroom home in {city}",
                address=f"{sample_addresses[i % len(sample_addresses)]}, {city}",
                city=city,
                district=district,
                size=size,
                price=price,
                bedrooms=bedrooms,
                rooms=rooms,
                bathrooms=random.choice([1, 2]),
                balconies=random.choice([0, 1, 2]),
                property_type=random.choice([c[0] for c in PropertyTypeChoices.choices]),
                build_year=random.choice([1998, 2005, 2012, 2018, 2022]),
                build_type=random.choice([c[0] for c in BuildTypeChoices.choices]),
                description="Sample listing generated for demo and UI testing.",
                heating=random.choice([c[0] for c in HeatingTypeChoices.choices]),
                exposure=exposure,
                floor=str(random.choice([1, 2, 3, 4, 5, 6, 7, 8])),
            )

            if amenities:
                chosen = random.sample(amenities, k=random.randint(0, min(3, len(amenities))))
                prop.amenities.set(chosen)

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {created} sample properties."))
