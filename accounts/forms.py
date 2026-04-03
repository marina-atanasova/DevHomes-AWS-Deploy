from django import forms
from django.utils import timezone

from .choices import MessageStatusChoices
from .models import UserInquiry


class ContactInquiryForm(forms.ModelForm):
    class Meta:
        model = UserInquiry
        fields = ["first_name", "last_name", "email", "phone", "listing", "message"]
        widgets = {
            "phone": forms.TextInput(attrs={
                "placeholder": "02/8123456 or +35988876556 or 0888445445"
            }),
            "message": forms.Textarea(attrs={
                "rows": 5
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user and user.is_authenticated:
            print(user)
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["phone"].initial = user.phone
        else:
            print ("No user")
class ContactForm(forms.ModelForm):

    class Meta:
        model = UserInquiry
        fields = "__all__"
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
            "reply_message": forms.Textarea(attrs={"rows": 4}),
            "replied_at": forms.DateTimeInput(attrs={"readonly": True}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "created_at" in self.fields:
            self.fields["created_at"].disabled = True
        if "posted_by" in self.fields:
            self.fields["posted_by"].disabled = True

    def save(self, commit=True):
        instance = super().save(commit=False)

        reply_text = (instance.reply_message or "").strip()

        if reply_text:
            instance.replied_at = timezone.now()
        else:
            instance.replied_at = None

        if instance.status == MessageStatusChoices.CLOSED:
            instance.closed_at = timezone.now()
        else:
            instance.closed_at = None

        if commit:
            instance.save()
            self.save_m2m()
        return instance