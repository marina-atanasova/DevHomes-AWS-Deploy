from django.test import TestCase
from django.urls import reverse

from Listings.forms import PropertyForm
from tests.data import VALID_LISTING_DATA
from tests.factories import create_broker, create_property
from tests.mixins import LoginMixin


class ListingBrokerIntegrityTest(LoginMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = create_broker(
            username="owner",
            email="owner@test.fd",
        )
        cls.other_broker = create_broker(
            username="otherbroker",
            email="other@test.sd",
        )
        cls.listing = create_property(
            broker=cls.owner,
            name="Test Listing",
            address="Old Address",
        )

    def test_broker_not_in_property_form(self):
        form = PropertyForm()
        self.assertNotIn("broker", form.fields)

    def test_broker_cannot_be_changed_through_update_post(self):
        self.login_user(self.owner)

        data = VALID_LISTING_DATA.copy()
        data["name"] = self.listing.name
        data["address"] = "New Address"

        # malicious attempt to transfer ownership
        data["broker"] = self.other_broker.id

        response = self.client.post(
            reverse("listings:edit", kwargs={"pk": self.listing.pk}),
            data=data,
        )

        self.assertEqual(response.status_code, 302)
        self.listing.refresh_from_db()

        self.assertEqual(self.listing.address, "New Address") # updated address successful

        self.assertEqual(self.listing.broker, self.owner) #verify broker is unchanged
        self.assertNotEqual(self.listing.broker, self.other_broker)