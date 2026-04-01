from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView

from .choices import MessageStatusChoices
from .forms import ContactInquiryForm, ContactForm
from .models import UserInquiry


@method_decorator(login_required, name="dispatch")
class ContactInquiryCreateView(CreateView):
    model = UserInquiry
    form_class = ContactInquiryForm
    template_name = "Accounts/contact_form.html"
    success_url = reverse_lazy("accounts:contact-dashboard")
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
class ContactInquiryUpdateView(UpdateView):
    model = UserInquiry
    form_class = ContactForm
    template_name = "Accounts/contact_edit.html"
    success_url = reverse_lazy("accounts:contact_dashboard")

    def dispatch(self, request, *args, **kwargs):
        inquiry = self.get_object()
        is_owner = inquiry.posted_by == request.user
        is_listing_broker = inquiry.listing.broker == request.user

        if request.user.is_superuser or is_owner or is_listing_broker:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied


class ContactInquiryListView(ListView):
    model = UserInquiry
    template_name = "Accounts/contact_dashboard.html"
    context_object_name = "inquiries"
    ordering = ['-created_at']
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get("status")

        if status in {choice[0] for choice in MessageStatusChoices.choices}:
            qs = qs.filter(status=status)

        if not status:
            qs = qs.exclude(status=MessageStatusChoices.CLOSED)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["selected_status"] = self.request.GET.get("status", "")
        ctx["status_choices"] = MessageStatusChoices.choices
        return ctx

class ContactInquiryDetailView(DetailView):
    model = UserInquiry
    template_name = "Accounts/contact_details.html"


@method_decorator(login_required, name="dispatch")
class ContactInquiryDeleteView(DeleteView):
    model = UserInquiry

    template_name = "Accounts/contact_delete_confirm.html"
    success_url = reverse_lazy("accounts:contact-dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Inquiry"
        return context

    def dispatch(self, request, *args, **kwargs):
        inquiry = self.get_object()
        is_owner = inquiry.posted_by == request.user
        is_listing_broker = inquiry.listing.broker == request.user

        if request.user.is_superuser or is_owner or is_listing_broker:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied
