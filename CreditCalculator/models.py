from django.conf import settings
from django.db import models

from Listings.models import Property


# Create your models here.

class CreditRequest(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_requests',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    property_price = models.FloatField()
    interest_rate = models.FloatField()
    down_payment = models.IntegerField()
    repayment_years = models.IntegerField()
    linked_property = models.ForeignKey(
        Property,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_requests'
    )

    def __str__(self):
        return f"Credit request {self.created_at:%Y-%m-%d}"


from django.conf import settings
from django.db import models


class CreditRequest(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_requests',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    property_price = models.FloatField()
    interest_rate = models.FloatField()
    down_payment = models.IntegerField()
    repayment_years = models.IntegerField()
    linked_property = models.ForeignKey(
        'Listings.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='credit_requests'
    )

    def __str__(self):
        return f"Credit request {self.created_at:%Y-%m-%d}"


class EarlyRepaymentReport(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PROCESSING = "processing"
    STATUS_READY = "ready"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PROCESSING, "Processing"),
        (STATUS_READY, "Ready"),
        (STATUS_FAILED, "Failed"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="early_repayment_reports",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    current_principal = models.DecimalField(max_digits=12, decimal_places=2)
    yearly_interest_rate = models.DecimalField(max_digits=6, decimal_places=2)
    years_left = models.PositiveIntegerField()
    monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)
    early_monthly_payment = models.DecimalField(max_digits=12, decimal_places=2)

    life_insurance_monthly = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    property_insurance_yearly = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    bank_fee_rate_yearly = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    pdf_file = models.FileField(
        upload_to="credit_reports/",
        null=True,
        blank=True,
    )
    error_message = models.TextField(blank=True)

    # optional cached summary fields
    total_paid_saved = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    interest_saved = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    extra_costs_saved = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    def __str__(self):
        return f"Early repayment report #{self.pk} - {self.status}"