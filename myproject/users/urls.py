from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginview, name="login"),
    path("register/", views.registerview, name="resgisterView"),
    path("logout/", views.logoutview, name="logout"),
]
