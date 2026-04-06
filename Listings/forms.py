from django import forms
from django.utils import timezone

from .choices import AptExposureChoices, CityChoices, DistrictChoices
from .models import Amenity, Property


class PropertyForm(forms.ModelForm):
    price_per_sqm = forms.DecimalField(
        label="Price per m²",
        required=False,
        disabled=True,
    )
    exposure = forms.MultipleChoiceField(
        choices=AptExposureChoices.choices,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        help_text="Select exposure(s): North, South, East, West.",
    )

    class Meta:
        model = Property
        exclude = ["broker"]
        widgets = {
            "amenities": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate the read-only field when editing an existing object
        if self.instance and self.instance.pk:
            value = self.instance.price_per_sqm
            self.fields["price_per_sqm"].initial = value

    def clean_build_year(self):
        year = self.cleaned_data.get("build_year")
        if year is None:
            return year
        current = timezone.now().year
        if year < 1800 or year > current + 10:
            raise forms.ValidationError(f"Build year must be between 1800 and {current + 10}.")
        return year

    def clean(self):
        cleaned = super().clean()
        address = cleaned.get("address")
        price = cleaned.get("price")
        exposure = cleaned.get("exposure")

        if not address:
            self.add_error(None, "Address cannot be blank.")

        if price is None:
            self.add_error(None, "Price cannot be blank.")

        if not exposure:
            self.add_error(None, "Please select at least one exposure.")
        return cleaned


class ListingsSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={"placeholder": "Search by name, address, city, district..."})
    )

    city = forms.ChoiceField(
        required=False,
        choices=[("", "Choose City")] + list(CityChoices.choices),
        label="City",
    )
    district = forms.ChoiceField(
        required=False,
        choices=[("", "Choose District")] + list(DistrictChoices.choices),
        label="District",
    )
    min_price = forms.IntegerField(
        required=False,
        min_value=0,
        label="Min price",
        widget=forms.NumberInput(attrs={"placeholder": 80000}),
    )

    max_price = forms.IntegerField(
        required=False,
        min_value=0,
        label="Max price",
        widget=forms.NumberInput(attrs={"placeholder": 200000}),
    )

    rooms = forms.IntegerField(
        required=False,
        min_value=0,
        label="Rooms",
        widget=forms.NumberInput(attrs={"placeholder": 3}),
    )

    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenity.objects.all().order_by("name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Amenities",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amenities"].queryset = Amenity.objects.all().order_by("name")

    def clean(self):
        cleaned = super().clean()
        min_price = cleaned.get("min_price")
        max_price = cleaned.get("max_price")

        if min_price is not None and max_price is not None and min_price > max_price:
            self.add_error("max_price", "Max price must be greater than or equal to Min price.")

        return cleaned


class AmenityForm(forms.ModelForm):
    class Meta:
        model = Amenity
        fields = "__all__"

        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Elevator"}),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Describe the amenity..."}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Amenity name must be at least 2 characters long.")
        return name
