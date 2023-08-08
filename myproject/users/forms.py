from django import forms
#from django.contrib.auth.models import User
from .models import CustomUser

class loginForm(forms.Form):
    email = forms.EmailField(label="", max_length=50)
    password = forms.CharField(label="", widget=forms.PasswordInput())

    email.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Email-id"}
    )
    password.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Password"}
    )


class UserRegisteration(forms.Form):
    class Meta:
        model = CustomUser

    fullName = forms.CharField(label="", max_length=100)
    emailAddress = forms.EmailField(label="")
    mobileNumber = forms.CharField(label="", max_length=10, min_length=10)
    password1 = forms.CharField(label="", widget=forms.PasswordInput(), min_length=6)
    password2 = forms.CharField(label="", widget=forms.PasswordInput(), min_length=6)

    fullName.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Your Full Name"}
    )
    emailAddress.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Email Address"}
    )
    mobileNumber.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Mobile Number"}
    )
    password1.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Password"}
    )
    password2.widget.attrs.update(
        {"class": "form-control", "placeholder": "Re-Enter Password"}
    )

    def clean_fullName(self):
        fullName = self.cleaned_data.get("fullName")
        return fullName

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Password Didn't matched")
        return password1

    def clean_emailAddress(self):
        emailAddress = self.cleaned_data.get("emailAddress")
        emailAddress = emailAddress.lower()
        qs = CustomUser.objects.filter(email=emailAddress)
        if qs.exists():
            raise forms.ValidationError("This emailAddress is already in use")
        return emailAddress

    def save(self, commit=True):
        user = super(UserRegisteration, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
