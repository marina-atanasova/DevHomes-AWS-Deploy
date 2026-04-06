
from django.test import TestCase
from django.urls import reverse

from tests.data import PASSWORD_RESET_DATA
from tests.factories import create_broker
from tests.mixins import LoginMixin
from users.models import User

class PasswordResetTest(LoginMixin, TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_broker()

    def test_change_valid_password(self):
        self.login_user(user=self.user)
        data = PASSWORD_RESET_DATA.copy()

        response = self.client.post(
            reverse('simple_password_reset'),
        data=data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass432"))
        self.assertFalse(self.user.check_password("testpass123"))
        self.assertEqual(response.status_code, 302)
        logged_in = self.client.login(
            username=self.user.username,
            password="newpass432"
        )
        self.assertTrue(logged_in)

    def test_change_password_with_invalid_username_fails(self):
        logged_in = self.client.login(
            username=self.user.username,
            password="testpass123"
        )
        self.assertTrue(logged_in)
        data = PASSWORD_RESET_DATA.copy()
        data['username'] = 'doesnotexist'

        response = self.client.post(
            reverse('simple_password_reset'),
        data=data)
        self.assertTrue(User.objects.filter(username="testbroker").exists())
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertTrue(logged_in)

    def test_change_password_with_unmatched_password_fails(self):
        logged_in = self.client.login(
            username="testbroker",
            password="testpass123"
        )
        self.assertTrue(logged_in)
        data = PASSWORD_RESET_DATA.copy()
        data['new_password2'] = 'nomatchpassword'
        response = self.client.post(
            reverse('simple_password_reset'),
        data=data)
        self.assertTrue(User.objects.filter(username=self.user.username).exists())
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("testpass123"))
        self.assertTrue(logged_in)

