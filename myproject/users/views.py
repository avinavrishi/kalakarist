from django.shortcuts import render, redirect
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "GET":
        return render(request, "sign-in/index.html", {"form": form, "invalid_user": False})
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                redirect_url = request.session.pop("redirectUrl", "home")
                return redirect(redirect_url)
            else:
                return render(request, "sign-in/index.html", {"form": form, "invalid_user": True})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = UserRegistrationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    return render(request, "register/register.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")
