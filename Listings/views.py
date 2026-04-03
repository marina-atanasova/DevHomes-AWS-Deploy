from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator

# Create your views here.

from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView

from users.decorators import allowed_groups
from users.models import UserRole
from .forms import PropertyForm
from django.shortcuts import render
from .models import Property, Amenity
from .forms import ListingsSearchForm, AmenityForm


class AllListings(ListView):
    model = Property
    paginate_by = 6

    context_object_name = "listings"
    template_name = "Listings/all_listings.html"

    def get_queryset(self):
        return Property.objects.all().order_by("-id")


def listings_search(request):
    form = ListingsSearchForm(request.GET or None)
    qs = Property.objects.all().order_by("-id")

    if request.GET and form.is_valid():
        q = form.cleaned_data.get("q")
        district = form.cleaned_data.get("district")
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        rooms = form.cleaned_data.get("rooms")
        amenities = form.cleaned_data.get("amenities")
        city = form.cleaned_data.get("city")

        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(address__icontains=q)
                | Q(city__icontains=q)
                | Q(district__icontains=q)
            )
        if city:
            qs = qs.filter(city=city)
        if district:
            qs = qs.filter(district=district)
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        if rooms is not None:
            qs = qs.filter(rooms__gte=rooms)
        if amenities:
            qs = qs.filter(amenities__in=amenities).distinct()


    return render(request, "Listings/search.html", {"form": form, "listings": qs})


class PropertyDetailView(DetailView):
    model = Property
    template_name = "Listings/property_detail.html"

@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class AddListingView(CreateView):
    model = Property
    form_class = PropertyForm
    template_name = "Listings/add_listing.html"
    success_url = "/listings"

    def form_valid(self, form):
        form.instance.broker = self.request.user
        return super().form_valid(form)

@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class EditListingView(UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = "Listings/edit_listing.html"
    success_url = "/listings"

    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()

        if request.user.is_superuser or listing.broker == request.user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied

@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class DeleteListingView(DeleteView):
    model = Property
    success_url = "/listings"
    template_name = "Listings/delete_listing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Listing"
        return context

    def dispatch(self, request, *args, **kwargs):
        listing = self.get_object()

        if request.user.is_superuser or listing.broker == request.user:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied


class AmenityListView(ListView):
    model = Amenity
    template_name = "Listings/all_amenities.html"
    context_object_name = "amenities"
    ordering = ["category", "name"]
    paginate_by = 6


@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class AmenityCreateView(CreateView):
    model = Amenity
    form_class = AmenityForm
    template_name = "Listings/add_amenity.html"
    success_url = '/listings/amenities'


@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class AmenityDetailView(DetailView):
    model = Amenity
    template_name = "Listings/amenity_detail.html"
    context_object_name = "amenity"


@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class AmenityUpdateView(UpdateView):
    model = Amenity
    form_class = AmenityForm
    template_name = "Listings/edit_amenity.html"
    success_url = '/listings/amenities'


@method_decorator(allowed_groups(["Broker"]), name="dispatch")
class AmenityDeleteView(DeleteView):
    model = Amenity
    template_name = "Listings/amenity_confirm_delete.html"
    success_url = '/listings/amenities'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Delete Amenity"
        return context


@login_required
def toggle_favorite(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.user.role not in [UserRole.CUSTOMER, UserRole.BROKER]:
        return HttpResponseForbidden("Only registered users can favorite listings.")

    if property_obj in request.user.favorite_properties.all():
        request.user.favorite_properties.remove(property_obj)
    else:
        request.user.favorite_properties.add(property_obj)

    return redirect("listings:detail", pk=pk)

