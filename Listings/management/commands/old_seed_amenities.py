from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import Amenity
from Listings.choices import AmenityCategoryChoices


class Command(BaseCommand):
    help = "Seed sample real estate amenities."

    @transaction.atomic
    def handle(self, *args, **options):
        amenities_data = [
            {
                "name": "Elevator",
                "category": AmenityCategoryChoices.BUILDING,
                "description": "Elevator access in the building.",
            },
            {
                "name": "Parking",
                "category": AmenityCategoryChoices.OUTDOOR,
                "description": "Dedicated parking space or nearby parking access.",
            },
            {
                "name": "Air Conditioning",
                "category": AmenityCategoryChoices.COMFORT,
                "description": "Cooling system installed in the property.",
            },
            {
                "name": "Security Door",
                "category": AmenityCategoryChoices.SECURITY,
                "description": "Reinforced front door for better protection.",
            },
            {
                "name": "Wheelchair Access",
                "category": AmenityCategoryChoices.ACCESSIBILITY,
                "description": "Step-free or adapted access for wheelchair users.",
            },
            {
                "name": "Basement",
                "category": AmenityCategoryChoices.BUILDING,
                "description": "Additional basement storage space.",
            },
            {
                "name": "Garden",
                "category": AmenityCategoryChoices.OUTDOOR,
                "description": "Private or shared garden area.",
            },
            {
                "name": "Furnished",
                "category": AmenityCategoryChoices.COMFORT,
                "description": "The property includes basic furniture.",
            },
        ]

        created = 0
        updated = 0

        for item in amenities_data:
            obj, was_created = Amenity.objects.update_or_create(
                name=item["name"],
                defaults={
                    "category": item["category"],
                    "description": item["description"],
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded amenities successfully. Created: {created}, updated: {updated}."
            )
        )
