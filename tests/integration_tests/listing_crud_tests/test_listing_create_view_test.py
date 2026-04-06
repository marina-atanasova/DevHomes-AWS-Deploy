from django.test import TestCase
from django.urls import reverse

from Listings.models import Property
from tests.data import VALID_LISTING_DATA
from tests.factories import create_broker, create_customer
from tests.mixins import LoginMixin

class ListingCreateViewTest(LoginMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_broker()
        cls.customer = create_customer()


    def test_create_listing_valid_data_broker(self):
        self.login_user(user=self.user)
        data = VALID_LISTING_DATA.copy()
        data['broker'] = self.user.id
        self.assertEqual(Property.objects.count(), 0)
        response = self.client.post(
            reverse('listings:add'),
            data=data,
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Property.objects.filter(
                name='Test Listing'
            ).exists()
        )
        self.assertTrue(Property.objects.filter(broker= self.user.id).exists())

    def test_create_listing_invalid_data_broker(self):
        self.login_user(user=self.user)
        data = VALID_LISTING_DATA.copy()
        data['build_year'] = 99
        response = self.client.post(
            reverse('listings:add'),
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Property.objects.filter(name= "Test Listing"))

    def test_create_listing_invalid_access_customer_fails(self):
        self.login_user(user=self.customer)
        data = VALID_LISTING_DATA.copy()
        data['broker'] = self.customer.id
        response = self.client.post(
            reverse('listings:add'),
            data=data,
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Property.objects.filter(name= "Test Listing"))