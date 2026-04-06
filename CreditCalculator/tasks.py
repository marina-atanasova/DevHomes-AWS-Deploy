from celery import shared_task
from django.core.files.base import ContentFile

from CreditCalculator.calculations import calculate_early_repayment_comparison
from CreditCalculator.models import EarlyRepaymentReport
from CreditCalculator.pdf_reports import build_early_repayment_pdf


@shared_task
def generate_early_repayment_report(report_id):
    report = EarlyRepaymentReport.objects.get(pk=report_id)

    report.status = EarlyRepaymentReport.STATUS_PROCESSING
    report.error_message = ""
    report.save(update_fields=["status", "error_message"])

    try:
        cleaned_data = {
            "current_principal": report.current_principal,
            "yearly_interest_rate": report.yearly_interest_rate,
            "years_left": report.years_left,
            "monthly_payment": report.monthly_payment,
            "early_monthly_payment": report.early_monthly_payment,
            "life_insurance_monthly": report.life_insurance_monthly,
            "property_insurance_yearly": report.property_insurance_yearly,
            "bank_fee_rate_yearly": report.bank_fee_rate_yearly,
        }

        results = calculate_early_repayment_comparison(
            principal=report.current_principal,
            yearly_interest_rate=report.yearly_interest_rate,
            monthly_payment=report.monthly_payment,
            early_monthly_payment=report.early_monthly_payment,
            life_insurance_monthly=report.life_insurance_monthly,
            property_insurance_yearly=report.property_insurance_yearly,
            bank_fee_rate_yearly=report.bank_fee_rate_yearly,
        )

        pdf_bytes = build_early_repayment_pdf(results, cleaned_data)

        filename = f"early_repayment_report_{report.pk}.pdf"
        report.pdf_file.save(filename, ContentFile(pdf_bytes), save=False)

        report.total_paid_saved = results["savings"]["total_paid_saved"]
        report.interest_saved = results["savings"]["interest_saved"]
        report.extra_costs_saved = results["savings"]["extra_costs_saved"]
        report.status = EarlyRepaymentReport.STATUS_READY
        report.save()

    except Exception as exc:
        report.status = EarlyRepaymentReport.STATUS_FAILED
        report.error_message = str(exc)
        report.save(update_fields=["status", "error_message"])
        raise