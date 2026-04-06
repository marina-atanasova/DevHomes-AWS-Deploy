from django.core.management.base import BaseCommand
from django.db import transaction

from Listings.models import City, District, Property
from Listings.choices import CityChoices


class Command(BaseCommand):
    help = "Seed Cities and City-specific Districts (no global DistrictChoices)."

    @transaction.atomic
    def handle(self, *args, **options):
        # Clear in safe order (district is PROTECTed by Property)
        Property.objects.all().delete()
        District.objects.all().delete()
        City.objects.all().delete()

        # Create cities
        cities = [
            CityChoices.SOFIA,
            CityChoices.PLOVDIV,
            CityChoices.VARNA,
            CityChoices.BURGAS,
            CityChoices.RUSE,
        ]
        city_objs = {c: City.objects.create(name=c) for c in cities}

        # City-specific districts
        districts_map = {
            CityChoices.SOFIA: ["Center", "Lozenets", "Mladost", "Drujba", "Borovo"],
            CityChoices.PLOVDIV: ["Center", "Kapana", "Trakia"],
            CityChoices.VARNA: ["Center", "Chayka", "Asparuhovo"],
            CityChoices.BURGAS: ["Center", "Lazur", "Sarafovo"],
            CityChoices.RUSE: ["Center", "Druzhba", "Zdravets"],
        }

        # Create districts
        for city_choice, names in districts_map.items():
            city = city_objs[city_choice]
            for name in dict.fromkeys(names):  # de-dupe just in case
                District.objects.create(city=city, name=name)

        self.stdout.write(self.style.SUCCESS("✅ Seeded cities and districts successfully."))