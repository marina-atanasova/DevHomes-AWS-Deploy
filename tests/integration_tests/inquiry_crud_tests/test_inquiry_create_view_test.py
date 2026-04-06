from django.test import TestCase
from django.urls import reverse

from accounts.models import UserInquiry
from tests.data import VALID_INQUIRY_DATA
from tests.factories import create_customer, create_property, create_broker
from tests.mixins import LoginMixin


class InquiryCreateTest(LoginMixin,TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_customer()
        cls.test_listing = create_property()
        cls.broker = create_broker()

    def test_create_inquiry_valid_data_user_logged_in(self):
        self.login_user(self.user)
        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.assertEqual(UserInquiry.objects.count(), 0)

        response = self.client.post(
            reverse('accounts:contact'),
            data=data,
        )

        self.assertTrue(
            UserInquiry.objects.filter(
                first_name='TestName',
            ).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_create_inquiry_valid_data_no_user_logged_in_fails(self):
        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.assertEqual(UserInquiry.objects.count(), 0)

        response = self.client.post(
            reverse('accounts:contact'),
            data=data,
        )
        self.assertFalse(
            UserInquiry.objects.filter(
                first_name='TestName',
            ).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_create_inquiry_valid_data_broker_logged_in(self):
        self.login_user(self.broker)
        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = self.test_listing.id

        self.assertEqual(UserInquiry.objects.count(), 0)

        response = self.client.post(
            reverse('accounts:contact'),
            data=data,
        )
        self.assertTrue(
            UserInquiry.objects.filter(
                first_name='TestName',
            ).exists()
        )
        self.assertEqual(response.status_code, 302)

    def test_create_inquiry_valid_data_no_listing_id_fails(self):
        self.login_user(self.user)
        data = VALID_INQUIRY_DATA.copy()
        data["listing"] = ''

        self.assertEqual(UserInquiry.objects.count(), 0)
        response = self.client.post(
            reverse('accounts:contact'),
            data=data,
        )
        self.assertFalse(
            UserInquiry.objects.filter(
                first_name='TestName',
            ).exists()
        )
        self.assertEqual(response.status_code, 200)

