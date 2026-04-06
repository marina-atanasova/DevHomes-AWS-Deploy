from django.test import TestCase

from CreditCalculator.forms import CreditCalculator
from tests.data import VALID_CREDIT_REQUEST_DATA
from tests.factories import create_property


class CreditRequestTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_listing = create_property()
    def test_credit_request_create_valid_data_no_property(self):
        form_data =  VALID_CREDIT_REQUEST_DATA.copy()
        form = CreditCalculator(data=form_data)
        self.assertTrue(form.is_valid())

    def test_credit_request_create_valid_data_test_property(self):
        form_data = VALID_CREDIT_REQUEST_DATA.copy()
        form_data['property'] = self.test_listing.id
        form = CreditCalculator(data=form_data)
        self.assertTrue(form.is_valid())

    def test_credit_request_create_invalid_data_test_property(self):
         #listing id doesn't exist
        form_data = VALID_CREDIT_REQUEST_DATA.copy()
        form_data['linked_property'] = 'wer'
        form = CreditCalculator(data=form_data)
        self.assertFalse(form.is_valid())