from django.test import TestCase

from Listings.forms import PropertyForm
from tests.data import VALID_LISTING_DATA


class ListingFormDataTests(TestCase):
    def test_property_form_missing_address_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["address"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_property_form_missing_build_year_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["build_year"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("build_year", form.errors)

    def test_property_form_missing_city_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["city"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("city", form.errors)

    def test_property_form_missing_district_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["district"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("district", form.errors)

    def test_property_form_missing_price_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["price"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("price", form.errors)

    def test_property_form_missing_exposure_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["exposure"] = ""

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)

    def test_property_form_invalid_exposure_invalid(self):
        data = VALID_LISTING_DATA.copy()
        data["exposure"] = "wer"

        form = PropertyForm(data=data)

        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)