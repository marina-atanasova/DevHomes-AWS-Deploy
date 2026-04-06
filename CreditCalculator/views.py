from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse, Http404, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from CreditCalculator.calculations import calculate_early_repayment_comparison
from CreditCalculator.forms import CreditCalculator, calculator, EarlyRepaymentCalculatorForm
from CreditCalculator.pdf_reports import build_early_repayment_pdf
from CreditCalculator.models import CreditRequest, EarlyRepaymentReport
from CreditCalculator.tasks import generate_early_repayment_report

# Create your views here.

def calculator_view(request):

    form = CreditCalculator(request.GET or None)
    context = {"form": form}


    if request.GET and form.is_valid():
        created_by = request.user if request.user.is_authenticated else None,
        property_price = form.cleaned_data.get("property_price")
        interest_rate_yearly = form.cleaned_data.get("interest_rate_yearly")
        self_funded_sum = form.cleaned_data.get("self_funded_sum")
        repayment_years = form.cleaned_data.get("repayment_years")
        linked_property = form.cleaned_data.get("linked_property")


        CreditRequest.objects.create(
            property_price=property_price,
            interest_rate=interest_rate_yearly,
            down_payment=self_funded_sum,
            repayment_years=repayment_years,
            linked_property=linked_property,
            created_by = request.user if request.user.is_authenticated else None

        )

        monthly_payment = calculator(property_price, interest_rate_yearly, self_funded_sum, repayment_years)
        loan_amount = property_price - self_funded_sum
        context.update({
            "monthly_payment": monthly_payment,
            "loan_amount": loan_amount,
            "self_funded_sum": self_funded_sum,
        })

    return render(request, "CreditCalculator/calculator.html", context)

def early_repayment_calculator_view(request):
    form = EarlyRepaymentCalculatorForm(request.GET or None)
    context = {"form": form}

    if request.GET and form.is_valid():
        try:
            results = calculate_early_repayment_comparison(
                principal=form.cleaned_data["current_principal"],
                yearly_interest_rate=form.cleaned_data["yearly_interest_rate"],
                monthly_payment=form.cleaned_data["monthly_payment"],
                early_monthly_payment=form.cleaned_data["early_monthly_payment"],
                life_insurance_monthly=form.cleaned_data.get("life_insurance_monthly"),
                property_insurance_yearly=form.cleaned_data.get("property_insurance_yearly"),
                bank_fee_rate_yearly=form.cleaned_data.get("bank_fee_rate_yearly"),
            )
            context.update(results)
        except ValueError as exc:
            form.add_error(None, str(exc))

    return render(request, "CreditCalculator/early_repayment_calculator.html", context)


class AllCreditRequests(generic.ListView):
    model = CreditRequest
    context_object_name = "credit_requests"
    template_name = "CreditCalculator/credit_all.html"

@method_decorator (login_required, name="dispatch")
class DeleteCreditRequest(generic.DeleteView):
    model = CreditRequest
    template_name = "CreditCalculator/credit_delete.html"
    success_url = reverse_lazy("CreditCalculator:credit_all")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Credit Request"
        return context

    def dispatch(self, request, *args, **kwargs):
        credit_request = self.get_object()
        is_owner = credit_request.created_by == request.user


        if request.user.is_superuser or is_owner:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied


def early_repayment_report_pdf_view(request):
    form = EarlyRepaymentCalculatorForm(request.GET or None)

    if not request.GET or not form.is_valid():
        return HttpResponse("Invalid data for PDF report.", status=400)

    results = calculate_early_repayment_comparison(
        principal=form.cleaned_data["current_principal"],
        yearly_interest_rate=form.cleaned_data["yearly_interest_rate"],
        monthly_payment=form.cleaned_data["monthly_payment"],
        early_monthly_payment=form.cleaned_data["early_monthly_payment"],
        life_insurance_monthly=form.cleaned_data.get("life_insurance_monthly"),
        property_insurance_yearly=form.cleaned_data.get("property_insurance_yearly"),
        bank_fee_rate_yearly=form.cleaned_data.get("bank_fee_rate_yearly"),
    )

    pdf_bytes = build_early_repayment_pdf(results, form.cleaned_data)

    filename = f"early_repayment_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response

@login_required
def early_repayment_report_request_view(request):
    form = EarlyRepaymentCalculatorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        report = EarlyRepaymentReport.objects.create(
            created_by=request.user,
            current_principal=form.cleaned_data["current_principal"],
            yearly_interest_rate=form.cleaned_data["yearly_interest_rate"],
            years_left=form.cleaned_data["years_left"],
            monthly_payment=form.cleaned_data["monthly_payment"],
            early_monthly_payment=form.cleaned_data["early_monthly_payment"],
            life_insurance_monthly=form.cleaned_data.get("life_insurance_monthly"),
            property_insurance_yearly=form.cleaned_data.get("property_insurance_yearly"),
            bank_fee_rate_yearly=form.cleaned_data.get("bank_fee_rate_yearly"),
            status=EarlyRepaymentReport.STATUS_PENDING,
        )

        transaction.on_commit(
            lambda: generate_early_repayment_report.delay(report.pk)
        )

        return redirect("CreditCalculator:credit_early_repayment_report_detail", pk=report.pk)

    return render(
        request,
        "CreditCalculator/early_repayment_report_request.html",
        {"form": form},
    )


@login_required
def early_repayment_report_detail_view(request, pk):
    report = get_object_or_404(EarlyRepaymentReport, pk=pk)

    if report.created_by != request.user and not request.user.is_superuser:
        raise Http404()

    return render(
        request,
        "CreditCalculator/early_repayment_report_detail.html",
        {"report": report},
    )


@login_required
def early_repayment_report_download_view(request, pk):
    report = get_object_or_404(EarlyRepaymentReport, pk=pk)

    if report.created_by != request.user and not request.user.is_superuser:
        raise Http404()

    if report.status != EarlyRepaymentReport.STATUS_READY or not report.pdf_file:
        return HttpResponse("Report is not ready yet.", status=400)

    return FileResponse(
        report.pdf_file.open("rb"),
        as_attachment=True,
        filename=report.pdf_file.name.split("/")[-1],
    )