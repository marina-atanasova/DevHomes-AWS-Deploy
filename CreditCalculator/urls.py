from django.urls import path
from . import views
from .views import DeleteCreditRequest

app_name = "CreditCalculator"

urlpatterns = [
    path("credit/", views.calculator_view, name="credit"),
    path("credit/all/", views.AllCreditRequests.as_view(), name="credit_all"),
    path("credit/<int:pk>/delete", DeleteCreditRequest.as_view(), name="credit_delete"),
    path("credit/early-repayment/", views.early_repayment_calculator_view, name="credit_early_repayment"),
    path(
        "credit/early-repayment/report/request/",
        views.early_repayment_report_request_view,
        name="credit_early_repayment_report_request",
    ),
    path(
        "credit/early-repayment/report/<int:pk>/",
        views.early_repayment_report_detail_view,
        name="credit_early_repayment_report_detail",
    ),
    path(
        "credit/early-repayment/report/<int:pk>/download/",
        views.early_repayment_report_download_view,
        name="credit_early_repayment_report_download",
    ),
]