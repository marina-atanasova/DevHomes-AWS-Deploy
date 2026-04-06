from django.test import TestCase
from django.urls import reverse

from Listings.models import Property
from tests.data import VALID_LISTING_DATA
from tests.factories import create_broker, create_property, create_customer
from tests.mixins import LoginMixin

class ListingCreateViewTest(LoginMixin ,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_broker()
        cls.customer = create_customer()
        cls.test_listing = create_property(
            broker=cls.user
        )

    def test_listing_update_success_view(self):
        self.login_user(self.user)

        data = VALID_LISTING_DATA.copy()
        data["address"] = "NEW ADDRESS"
        data["broker"] = self.user.id

        self.assertEqual(Property.objects.all().count(), 1)
        self.assertTrue(
            Property.objects.filter(
                name='Test Listing',
                address='Test Address',
            ).exists()
        )
        response = self.client.post(
            reverse("listings:edit", kwargs={"pk": self.test_listing.id}),
            data=data,
        )
        self.assertTrue(
            Property.objects.filter(
                name='Test Listing',
                address='NEW ADDRESS',
            ).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_listing_update_no_permissions_fails(self):
        self.login_user(self.customer)
        data = VALID_LISTING_DATA.copy()
        data["address"] = "NEW ADDRESS"
        data["broker"] = self.customer.id

        response = self.client.post(
            reverse("listings:edit", kwargs={"pk": self.test_listing.id}),
            data=data,
        )
        self.assertEqual(response.status_code, 403)

    def test_listing_update_no_permissions_wrong_broker_fails(self):
        self.new_broker = create_broker(email = "broker2@sd.sd", username = "user2")
        self.login_user(self.new_broker)
        data = VALID_LISTING_DATA.copy()
        data["address"] = "change"

        response = self.client.post(
            reverse("listings:edit", kwargs={"pk": self.test_listing.id}),
            data=data,
        )
        self.assertFalse(Property.objects.filter(address = 'change').exists())
        self.assertEqual(response.status_code, 403)