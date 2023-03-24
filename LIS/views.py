from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
            return render(request, "admin_login.html", {'alert':alert})
    return render(request, "admin_login.html")

def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        department = request.POST['department']
        insti_id = request.POST['insti_id']
        category=request.POST['category']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "student_registration.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username=username, password=password,first_name=first_name, last_name=last_name)
        if category!="Faculty":
            student = Student.objects.create(user=user, full_name= first_name+last_name, email=email, phone=phone, department=department,insti_id=insti_id, category=category)
            user.save()
            student.save()
        else:
            faculty= Faculty.objects.create(user=user, full_name= first_name+last_name, email=email, phone=phone, department=department,insti_id=insti_id, category=category)
            user.save()
            faculty.save()
        alert = True
        return render(request, "registration.html", {'alert':alert})
    return render(request, "registration.html")

@login_required(login_url = '/admin_login')
def admin_index(request):
    render(request, '/admin_page')

@login_required(login_url = '/admin_login')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert':alert})
    return render(request, "add_book.html")