from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms

# Create your views here.


def index(request):
    return render(request, "index.html")


def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/add_book")
            else:
                return HttpResponse("You are not an admin.")
        else:
            alert = True
            return render(request, "admin_login.html", {'alert': alert})
    return render(request, "admin_login.html")


def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        department = request.POST['department']
        insti_id = request.POST['insti_id']
        category = request.POST['category']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match")

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        if category == "UG":
            ug = Undergraduate.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                              phone=phone, department=department, insti_id=insti_id, category=category)
            user.save()
            ug.save()
        if category == "PG":
            pg = Postgraduate.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                             phone=phone, department=department, insti_id=insti_id, category=category)
            user.save()
            pg.save()
        if category == "PG":
            rs = ResearchScholar.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                                phone=phone, department=department, insti_id=insti_id, category=category)
            user.save()
            rs.save()
        if category == "Faculty":
            faculty = Faculty.objects.create(user=user, first_name=first_name, last_name=last_name, email=email,
                                             phone=phone, department=department, insti_id=insti_id, category=category)
            user.save()
            faculty.save()
        alert = True
        return render(request, "registration.html", {'alert': alert})
    return render(request, "registration.html")