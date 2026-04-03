from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from users.models import User, UserRole


class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserRole.choices,
        widget=forms.RadioSelect,
        initial=UserRole.BROKER,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username","first_name", "last_name", "email", "phone", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)

        user.role = self.cleaned_data["role"]


        if user.role == UserRole.BROKER:
            user.is_staff = True
        else:
            user.is_staff = False

        if commit:
            user.save()

            group_name = user.get_role_display()  # "Broker" or "Customer"
            group, created = Group.objects.get_or_create(name=group_name)

            user.groups.clear()
            user.groups.add(group)

        return user

class SimplePasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150)
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput,
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("No user with this username exists.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

class UserProfileEditForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    role = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = ("username", "role", "first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields["role"].initial = self.instance.get_role_display()