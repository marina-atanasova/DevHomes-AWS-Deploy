from django.test import TestCase
from django.urls import reverse

from accounts.models import UserInquiry
from tests.data import VALID_INQUIRY_DATA
from tests.factories import create_property, create_customer, create_broker, create_inquiry


class TestUserRoleAssignmentAndPermissions(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.broker = create_broker()
        cls.other_broker = create_broker(username="other", email="other@test.com")
        cls.customer = create_customer()
        cls.test_listing = create_property(
            broker=cls.broker
        )

    def test_customer_can_create_inquiries(self):
        self.client.login(username=self.customer.username, password="testpass123")

        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.client.post(reverse("accounts:contact"), data=data)
        inquiry = UserInquiry.objects.first()
        self.assertEqual(inquiry.posted_by, self.customer)

    def test_not_logged_in_cannot_create_inquiries(self):
        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.client.post(reverse("accounts:contact"), data=data)
        inquiry = UserInquiry.objects.first()

        self.assertIsNone(inquiry)

    def test_broker_can_create_inquiries(self):
        self.client.login(username=self.broker.username, password="testpass123")

        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.client.post(reverse("accounts:contact"), data=data)
        inquiry = UserInquiry.objects.first()
        self.assertEqual(inquiry.posted_by, self.broker)

