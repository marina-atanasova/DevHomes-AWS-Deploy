from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DeleteView

from users.forms import UserRegisterForm, SimplePasswordResetForm, UserProfileEditForm
from users.models import User


# Create your views here.
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class SimplePasswordResetView(FormView):
    template_name = "users/password_reset.html"
    form_class = SimplePasswordResetForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        new_password = form.cleaned_data["new_password1"]

        user = User.objects.get(username=username)

        try:
            validate_password(new_password, user=user)
        except ValidationError as e:
            form.add_error("new_password1", e)
            return self.form_invalid(form)

        user.set_password(new_password)
        user.save()

        return super().form_valid(form)

@login_required
def dashboard(request):
    user = request.user

    context = {
        "user": user,
        "favorite_listings": user.favorite_properties.all(),
        "inquiries": user.inquiries.all(),
        "credit_requests": user.credit_requests.all(),
        "my_listings": user.broker_listings.all() if user.role == "broker" else [],

    }

    return render(request, "users/dashboard.html", context)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileEditForm
    template_name = "users/edit_profile.html"
    success_url = reverse_lazy("dashboard")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/profile_delete.html"
    success_url = reverse_lazy("login")

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Account"
        return context

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)