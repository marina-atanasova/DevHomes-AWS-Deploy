from django.test import TestCase

from tests.factories import create_property, create_customer, create_broker


class TestUserRoleAssignmentAndPermissions(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.broker = create_broker()
        cls.other_broker = create_broker(username="other", email="other@test.com")
        cls.customer = create_customer()
        cls.test_listing = create_property(
            broker=cls.broker
        )
    def test_broker_is_broker(self):
        self.assertTrue(self.broker.is_broker())
        self.assertFalse(self.broker.is_customer())

    def test_customer_is_customer(self):
        self.assertTrue(self.customer.is_customer())

    def test_listing_owner_broker_can_edit(self):
        listing = create_property(broker=self.broker)
        self.assertEqual(listing.broker, self.broker)

    def test_other_broker_cant_edit_listing(self):
        listing = create_property(broker=self.broker)
        self.assertNotEqual(listing.broker, self.other_broker)

    def test_customer_cant_edit_listing(self):
        listing = create_property(broker=self.other_broker)
        self.assertNotEqual(listing.broker, self.customer)




