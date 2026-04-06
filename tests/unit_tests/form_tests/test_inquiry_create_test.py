from django.test import TestCase

from Listings.models import Property
from accounts.forms import ContactInquiryForm
from tests.data import VALID_INQUIRY_DATA
from tests.factories import create_property


class InquiryCreateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_listing = create_property()
    def test_inquiry_create_valid_listing(self):
        form_data = VALID_INQUIRY_DATA.copy()
        form_data['listing'] = self.test_listing.id
        form = ContactInquiryForm(data=form_data)
        self.assertTrue(form.is_valid())
    def test_inquiry_create_invalid_listing(self):
        form_data = VALID_INQUIRY_DATA.copy()
        form_data['listing'] = 'sdf'
        form = ContactInquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
    def test_inquiry_create_valid_listing_invalid_phone(self):
        form_data = VALID_INQUIRY_DATA.copy()
        form_data['phone'] = '8765432765432' # phone too long
        form_data['listing'] = self.test_listing.id

        form = ContactInquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data['phone'] = 'asderer' #phone not numeric
        form = ContactInquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
        form_data['phone'] = '345'  # phone too short
        form = ContactInquiryForm(data=form_data)
        self.assertFalse(form.is_valid())