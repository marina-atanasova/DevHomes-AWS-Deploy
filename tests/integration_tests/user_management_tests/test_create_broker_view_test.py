from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from tests.data import VALID_BROKER_DATA
from users.models import User


class CustomerCreateTest(TestCase):

    def test_valid_broker_create_profile_view(self):
        data = VALID_BROKER_DATA.copy()
        response = self.client.post(
            reverse('register'),
            data = data
        )
        self.assertTrue(
            User.objects.filter(username = 'TestBroker', role='broker').exists()
        )
        self.assertEqual(response.status_code, 302)
    def test_invalid_password_broker_create_view_fails(self):
        data = VALID_BROKER_DATA.copy()
        data['password2'] = 'asdasdasd'
        response = self.client.post(
            reverse('register'),
            data=data
        )
        self.assertFalse(User.objects.filter(username = 'TestBroker', role='broker').exists()
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_phone_broker_create_view_fails(self):
        data = VALID_BROKER_DATA.copy()
        data['phone'] = 'asdasdasd'
        response = self.client.post(
            reverse('register'),
            data=data
        )
        self.assertFalse(User.objects.filter(username = 'TestBroker', role='broker').exists()
        )
        self.assertEqual(response.status_code, 200)

    def test__broker_create_view_fails_email_already_exists(self):
        data = VALID_BROKER_DATA.copy()
        data['email'] = 'asd@asd.asd'
        response1 = self.client.post(
            reverse('register'),
            data=data
        )
        self.assertEqual(response1.status_code, 302)
        self.client.logout()
        second_response = self.client.post(
            reverse('register'),
            data=data
        )
        self.assertEqual(User.objects.filter(email="asd@asd.asd").count(), 1)
        if second_response.context and "form" in second_response.context:
            self.assertTrue(second_response.context["form"].errors)
        self.assertEqual(second_response.status_code, 200)