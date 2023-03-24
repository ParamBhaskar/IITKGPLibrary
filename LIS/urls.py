from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin_login/", views.admin_login, name="admin_login"),
    path("registration/", views.registration, name="registration"),
]