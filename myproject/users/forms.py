from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField(label="", max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Email"}))
    password = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"}))

    email.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Email-id"}
    )
    password.widget.attrs.update(
        {"class": "form-control", "placeholder": "Enter Password"}
    )
    
    
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number']

    email = forms.EmailField(label="", widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter Email Address"}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your First Name"}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Your Last Name"}))
    phone_number = forms.CharField(label="", max_length=10, min_length=10, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Mobile Number"}))
    #role = forms.ChoiceField(label="", choices=CustomUser.ROLES, widget=forms.Select(attrs={"class": "form-control"}))
    # tnc_acceptance = forms.BooleanField(label="Accept Terms and Conditions", required=True)

    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter Password"}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Re-Enter Password"}))

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number should only contain digits.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get("email")
        email = email.lower()
        qs = CustomUser.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
