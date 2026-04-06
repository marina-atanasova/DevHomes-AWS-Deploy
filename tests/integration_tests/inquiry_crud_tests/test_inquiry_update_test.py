from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import UserInquiry
from accounts.choices import MessageStatusChoices
from tests.factories import (
    create_broker,
    create_customer,
    create_property,
    create_inquiry,
)
from tests.mixins import LoginMixin


class ContactInquiryUpdateViewTests(LoginMixin, TestCase):
    def setUp(self):
        self.broker = create_broker()
        self.owner = create_customer(username="owner", email="owner@test.com")
        self.other_user = create_customer(username="other", email="other@test.com")

        self.listing = create_property(broker=self.broker)
        self.inquiry = create_inquiry(
            posted_by=self.owner,
            listing=self.listing,
        )
        self.url = reverse("accounts:contact-edit", kwargs={"pk": self.inquiry.pk})

    def test_owner_can_access_edit_page(self):
        self.login_user(self.owner)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_listing_broker_can_access_edit_page(self):
        self.login_user(self.broker)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_another_customer_user_cannot_access_edit_page(self):
        self.login_user(self.other_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_owner_can_reply_to_inquiry(self):
        self.login_user(self.owner)

        response = self.client.post(self.url, data={
            "posted_by": self.owner.pk,
            "first_name": self.inquiry.first_name,
            "last_name": self.inquiry.last_name,
            "phone": self.inquiry.phone,
            "email": self.inquiry.email,
            "listing": self.listing.pk,
            "request_type": self.inquiry.request_type,
            "message": self.inquiry.message,
            "status": MessageStatusChoices.NEW,
            "reply_message": "Thanks, we will contact you soon.",
        })

        self.assertRedirects(response, reverse("accounts:contact-dashboard"))

        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.reply_message, "Thanks, we will contact you soon.")
        self.assertIsNotNone(self.inquiry.replied_at)
        self.assertIsNone(self.inquiry.closed_at)

    def test_empty_reply_clears_replied_at(self):
        self.inquiry.reply_message = "Old reply"
        self.inquiry.replied_at = timezone.now()
        self.inquiry.save()

        self.login_user(self.owner)

        response = self.client.post(self.url, data={
            "posted_by": self.owner.pk,
            "first_name": self.inquiry.first_name,
            "last_name": self.inquiry.last_name,
            "phone": self.inquiry.phone,
            "email": self.inquiry.email,
            "listing": self.listing.pk,
            "request_type": self.inquiry.request_type,
            "message": self.inquiry.message,
            "status": MessageStatusChoices.NEW,
            "reply_message": "",
        })

        self.assertRedirects(response, reverse("accounts:contact-dashboard"))

        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.reply_message, "")
        self.assertIsNone(self.inquiry.replied_at)

    def test_closed_status_sets_closed_at(self):
        self.login_user(self.broker)

        response = self.client.post(self.url, data={
            "posted_by": self.owner.pk,
            "first_name": self.inquiry.first_name,
            "last_name": self.inquiry.last_name,
            "phone": self.inquiry.phone,
            "email": self.inquiry.email,
            "listing": self.listing.pk,
            "request_type": self.inquiry.request_type,
            "message": self.inquiry.message,
            "status": MessageStatusChoices.CLOSED,
            "reply_message": "Resolved.",
        })

        self.assertRedirects(response, reverse("accounts:contact-dashboard"))

        self.inquiry.refresh_from_db()
        self.assertEqual(self.inquiry.status, MessageStatusChoices.CLOSED)
        self.assertIsNotNone(self.inquiry.closed_at)
        self.assertIsNotNone(self.inquiry.replied_at)