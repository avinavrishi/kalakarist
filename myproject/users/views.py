from django.shortcuts import render, redirect
from .forms import loginForm, UserRegisteration
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.models import User


# Create your views here.
def loginview(request):
    
    form = loginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "GET":
        return render(
            request, "sign-in/index.html", {"form": form, "invalid_user": False}
        )
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            pas = form.cleaned_data.get("password")
            user = authenticate(email=email, password=pas)
            if user != None:
                login(request, user)
                if "redirectUrl" in request.session:
                    redirectUrl = request.session["redirectUrl"]
                    del request.session["redirectUrl"]
                else:
                    redirectUrl = "home"

                return redirect(redirectUrl)

            else:
                return render(
                    request, "sign-in/index.html", {"form": form, "invalid_user": True}
                )


def registerview(request):
    # CHECK USER AUTHENTICATIONS
    if request.user.is_authenticated:
        return redirect("home")
    form = UserRegisteration(request.POST or None)
    if form.is_valid():
        password1 = form.cleaned_data.get("password1")
        password2 = form.cleaned_data.get("password2")
        if password1 != password2:
            return render(
                request,
                "register.html",
                {"form": form, "error": "Password doesn't match"},
            )
        else:
            password = password1
        fullName = form.cleaned_data.get("fullName")
        emailAddress = form.cleaned_data.get("emailAddress")
    return render(request, "register/register.html", {"form": form})


def logoutview(request):
    logout(request)
    return redirect("home")
