from django.test import TestCase

from Listings.forms import AmenityForm
from Listings.models import Property


class AmenityCreateTest(TestCase):
    def test_amenity_create_valid_data(self):
        form_data = {
            'name': 'Staircase',
            'category': 'Accessibility',
            'description': 'Test Description',
        }
        form = AmenityForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_amenity_create_invalid_data(self):
        form_data = {
            'name': 'Staircase',
            'category': 'invalid_categoru', #invalid category name
            'description': 'Test Description',
        }
        form = AmenityForm(data=form_data)
        self.assertFalse(form.is_valid())