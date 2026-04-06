from django.test import TestCase

from Listings.models import Property
from tests.factories import create_amenity, create_property


class ListingTests(TestCase):
    def test_listing_create_valid_data_saved(self):
        listing = create_property()

        listing.full_clean()

        self.assertIsNotNone(listing.pk)
        self.assertTrue(Property.objects.filter(pk=listing.pk).exists())

    def test_listing_create_valid_data_with_amenity_assigned(self):
        amenity = create_amenity()
        listing = create_property(amenities=[amenity])

        listing.full_clean()

        self.assertIsNotNone(listing.pk)
        self.assertTrue(Property.objects.filter(pk=listing.pk).exists())
        self.assertEqual(listing.amenities.count(), 1)
        self.assertIn(amenity, listing.amenities.all())

    def test_listing_create_valid_data_without_amenities(self):
        listing = create_property()

        listing.full_clean()

        self.assertIsNotNone(listing.pk)
        self.assertEqual(listing.amenities.count(), 0)

    def test_price_per_sqm_calculation_is_valid(self):
        listing = create_property(price=100000, size=100)

        self.assertEqual(float(listing.price_per_sqm), 1000.00)

    def test_price_per_sqm_with_zero_size_returns_none(self):
        listing = create_property(price=100000, size=0)

        self.assertIsNone(listing.price_per_sqm)

    def test_property_str(self):
        listing = create_property(name="Nice Home Name Listing")

        self.assertEqual(str(listing), "Nice Home Name Listing")