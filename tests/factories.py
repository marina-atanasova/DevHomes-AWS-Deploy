from django.contrib.auth.models import Group

from Listings.models import Property, Amenity
from accounts.models import UserInquiry
from tests.data import VALID_LISTING_DATA, VALID_INQUIRY_DATA, VALID_AMENITY_DATA
from users.models import User


def create_broker(**kwargs):
    defaults = {
        "username": "testbroker",
        "email": "broker@test.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Broker",
        "phone": "0888444555",
    }
    defaults.update(kwargs)

    password = defaults.pop("password")

    user = User.objects.create_user(password=password, **defaults)

    if hasattr(user, "role"):
        user.role = "broker"
        user.save()

    group, _ = Group.objects.get_or_create(name="Broker")
    user.groups.add(group)

    return user

def create_customer(**kwargs):
    defaults = {
        "username": "testcustomer",
        "email": "customer@test.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "Customer",
        "phone": "0888444555",
    }
    defaults.update(kwargs)
    password = defaults.pop("password")
    user = User.objects.create_user(password=password, **defaults)

    # optional custom role field
    if hasattr(user, "role"):
        user.role = "customer"
        user.save()

    group, _ = Group.objects.get_or_create(name="Customer")
    user.groups.add(group)

    return user



def create_inquiry(**kwargs):
    data = VALID_INQUIRY_DATA.copy()
    data.update(kwargs)
    return UserInquiry.objects.create(**data)

def create_amenity(**kwargs):
    data = VALID_AMENITY_DATA.copy()
    data.update(kwargs)
    return Amenity.objects.create(**data)

def create_property(**kwargs):
    data = VALID_LISTING_DATA.copy()
    data.update(kwargs)
    amenities = data.pop("amenities", None)
    listing = Property.objects.create(**data)

    if amenities is not None:
        listing.amenities.set(amenities)
    return listing