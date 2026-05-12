from django import forms
from django.contrib.auth import authenticate
from .models import User


class Step1Form(forms.Form):
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "John Doe"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={"placeholder": "+1 (555) 000-0000"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Min 8 characters"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Repeat password"}))

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cd = super().clean()
        if cd.get("password") != cd.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")
        return cd


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "you@example.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cd = super().clean()
        email = cd.get("email")
        password = cd.get("password")
        if email and password:
            self.user = authenticate(self.request, username=email, password=password)
            if not self.user:
                raise forms.ValidationError("Invalid email or password.")
        return cd
