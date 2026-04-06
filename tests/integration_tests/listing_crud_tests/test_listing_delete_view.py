from django.test import TestCase
from django.urls import reverse

from Listings.models import Property
from tests.factories import create_broker, create_property, create_customer
from tests.mixins import LoginMixin

class ListingDeleteViewTest(LoginMixin ,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_broker()
        cls.customer = create_customer()
        cls.new_broker = create_broker(email = "broker2@sd.sd", username = "user2")
        cls.test_listing = create_property(
            broker=cls.user
        )

    def test_listing_delete_get_view_get_confirmation_page(self):
        self.login_user(self.user)


        response = self.client.get(
            reverse("listings:delete", kwargs={"pk": self.test_listing.id}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Property.objects.filter(pk=self.test_listing.pk).exists())

    def test_delete_listing_owner_post_deletes(self):
        self.login_user(self.user)

        response = self.client.post(
            reverse("listings:delete", kwargs={"pk": self.test_listing.pk})
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Property.objects.filter(pk=self.test_listing.pk).exists())


    def test_listing_delete_broker_no_permissions_fails(self):
        self.login_user(self.new_broker)

        response = self.client.post(
            reverse("listings:delete", kwargs={"pk": self.test_listing.pk})
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Property.objects.filter(pk=self.test_listing.pk).exists())

    def test_listing_delete_customer_no_permissions_fails(self):
        self.login_user(self.customer)

        response = self.client.post(
            reverse("listings:delete", kwargs={"pk": self.test_listing.pk})
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Property.objects.filter(pk=self.test_listing.pk).exists())

