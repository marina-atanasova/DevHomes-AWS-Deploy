from django.db.models.functions import Round
from django.shortcuts import render
from django.db.models import Count, Avg
from Listings.models import Property
from accounts.models import UserInquiry
from CreditCalculator.models import CreditRequest


def home(request):
    total_listings = Property.objects.all().count()
    total_inquiries = UserInquiry.objects.count()
    total_credit_requests = CreditRequest.objects.count()

    most_recent_property = (
        Property.objects
        .order_by("-id")
        .first()
    )

    most_credit_property = (
        Property.objects
        .annotate(credit_requests_count=Count("credit_requests"))
        .filter(credit_requests_count__gt=0)
        .order_by("-credit_requests_count", "-id")
        .first()
    )

    most_inquiry_property = (
        Property.objects
        .annotate(inquiries_count=Count("inquiries"))
        .filter(inquiries_count__gt=0)
        .order_by("-inquiries_count", "-id")
        .first()
    )

    recent_inquiries = (
        UserInquiry.objects.select_related("listing")
        .order_by("-created_at")[:3]
    )

    credit_stats = CreditRequest.objects.aggregate(
        avg_credit_requested=Round(Avg("property_price"), 2),
        avg_credit_years=Round(Avg("repayment_years"), 2),
    )

    context = {
        "total_listings": total_listings,
        "total_inquiries": total_inquiries,
        "total_credit_requests": total_credit_requests,
        "most_recent_property": most_recent_property,
        "most_credit_property": most_credit_property,
        "most_inquiry_property": most_inquiry_property,
        "recent_inquiries": recent_inquiries,
        "avg_credit_requested": credit_stats["avg_credit_requested"],
        "avg_credit_years": credit_stats["avg_credit_years"],
        "form_view":"core.home view OK"
    }

    return render(request, "home.html", context)


def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)