from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import date
import socket
from . import forms, models

import random
from django.conf import settings

from django.core.mail import EmailMessage

def f_p(request):
    return render(request, 'f_p.html')
def send_otp(request):
    error_message= None
    otp=random.randint(100000,999999)
    email=request.POST.get('email')
    user_email=User.objects.filter(email=email)
    if user_email:
        user=User.objects.get(email=email)
        user.otp =otp
        user.save()
        request.session['email']= request.POST['email']
        subject = "Request for change password of LIS profile"
        html_message="Your One Time password : - " + "" + str(otp)
        email_from= "paramanandabhaskar@gmail.com"
        email_to=[email]
        message= EmailMessage(subject, html_message,email_from,email_to)
        message.send()
        
        return redirect('enter_otp')

    else:
        # error_message="Invalid Email !!! Please Enter correct Email"
        alert= True
        return render(request, 'f_p.html', {'alert': alert})
    
def enter_otp(request):
    error_message = None
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.filter(email=email)
        for u in user:
            user_otp = u.otp
        if request.method == "POST":
            otp = request.POST.get('otp')
            request.user = User.objects.get(otp=user_otp)
            user = User.objects.get(otp=user_otp)
            if not otp:
                error_message = "OTP is required"
            elif not user_otp == otp:
                error_message = "OTP is invalid"
            if not error_message:
                if request.user.is_superuser:
                    pass
                else:
                    # return render(request, "/forgot_password/", {'user': user})
                    return redirect('forgot_password')
        return render(request, 'enter_otp.html', {'error': error_message})
    
    else:
        return render(request, "f_p.html")

def forgot_password(request):
    if request.session.has_key('email'):
        email = request.session['email']
        request.user=User.objects.get(email=email)
        user = User.objects.get(email=email)
        if request.method == "POST":
            new_password = request.POST['new_password']
            try:
                u = User.objects.get(id=request.user.id)
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "forgot_password.html", {'alert': alert})
            except:
                pass
    return render(request, "forgot_password.html")

def index(request):
    return render(request, "index.html")


# def clerk_login(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)

#         if user is not None:
#             login(request, user)
#             if request.user.is_superuser:
#                 return redirect("/add_book")
#             else:
#                 return HttpResponse("You are not an admin.")
#         else:
#             alert = True
#             return render(request, "clerk_login.html", {'alert': alert})
#     return render(request, "clerk_login.html")


def reg(request):
    if request.method == "POST":
        # username = request.POST['username']
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
            insti_id=insti_id, email=email, password=password, first_name=first_name, last_name=last_name)

        if category == "Faculty":
            faculty = Faculty.objects.create(user=user, first_name=first_name, last_name=last_name,
                                             phone=phone, department=department, category=category,insti_id=insti_id,book_limit=10)
            user.save()
            faculty.save()
        else:
            student = Student.objects.create(user=user, first_name=first_name, last_name=last_name, phone=phone, department=department, category=category,insti_id=insti_id)
            if student.category== "UG":
                student.book_limit=2
            if student.category== "PG":
                student.book_limit=4
            if student.category== "RS":
                student.book_limit=6              
            user.save()
            student.save()

        alert = True

        return render(request, "reg.html", {'alert': alert})
    return render(request, "reg.html")


def login_karo(request):
    if request.method == "POST":
        insti_id = request.POST['insti_id']
        password = request.POST['password']
        user = authenticate(insti_id=insti_id, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return redirect("/admin")
            else:
                if len(user.insti_id)!= 5:
                    return redirect("/afterlogin")
                    
                else:
                    return redirect("/add_book")
        else:
            alert = True
            return render(request, "login.html", {'alert': alert})
    return render(request, "login.html")


def profile(request):
    return render(request, "profile.html")

@login_required(login_url='/login')
def afterlogin(request):
    return render(request, "afterlogin.html")


@login_required(login_url='/login')
def edit_profile(request):
    student = Student.objects.get(user=request.user)
    # student = Undergraduate.objects.get(user=request.user) or Postgraduate.objects.get(
    #     user=request.user) or ResearchScholar.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        insti_id = request.POST['insti_id']

        student.user.email = email
        student.phone = phone
        student.department = department
        student.insti_id = insti_id
        student.user.save()
        student.save()
        alert = True
        return render(request, "edit_profile.html", {'alert': alert})
    return render(request, "edit_profile.html")


@login_required(login_url='/login')
def student_issued_books(request):
    student = Student.objects.filter(user_id=request.user.id)
    issuedBooks = IssuedBook.objects.filter(student_id=student[0].user_id)
    li1 = []
    li2 = []

    for i in issuedBooks:
        books = Book.objects.filter(isbn=i.isbn)
        for book in books:
            t = (request.user.id, request.user.get_full_name,
                 book.name, book.author)
            li1.append(t)

        days = (date.today()-i.issued_date)
        d = days.days
        fine = 0
        if student[0].category == "UG":
            if d > 30:
                day = d-30
                fine = day*10
        if student[0].category == "PG":
            if d > 30:
                day = d-30
                fine = day*10
        if student[0].category == "RS":
            if d > 90:
                day = d-90
                fine = day*10
        if student[0].category == "Faculty":
            if d > 180:
                day = d-180
                fine = day*10
        t = (issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
        li2.append(t)
    return render(request, 'student_issued_books.html', {'li1': li1, 'li2': li2})


# @login_required(login_url='/clerk_login')
# def issue_book(request):
#     form = forms.IssueBookForm()
#     if request.method == "POST":
#         form = forms.IssueBookForm(request.POST)
#         if form.is_valid():
#             obj = models.IssuedBook()
#             obj.student_id = request.POST['name2']
#             obj.isbn = request.POST['isbn2']
#             obj.save()
#             alert = True
#             return render(request, "issue_book.html", {'obj': obj, 'alert': alert})
#     return render(request, "issue_book.html", {'form': form})

@login_required(login_url='login/clerk_login/')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    details = []
    for i in issuedBooks:
        days = (date.today()-i.issued_date)
        d = days.days
        fine = 0
        if d > 14:
            day = d-14
            fine = day*5
        books = list(models.Book.objects.filter(isbn=i.isbn))
        students = list(models.Student.objects.filter(user=i.student_id))
        i = 0
        for l in books:
            t = (students[i].user, students[i].user_id, books[i].name, books[i].isbn,
                 issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
            i = i+1
            details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks': issuedBooks, 'details': details})


def Logout(request):
    logout(request)
    return redirect("/")


@login_required(login_url='login/clerk_login/')
def add_book(request):
    if request.method == "POST":
        name = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        rack_no = request.POST['rack_no']
        copies = request.POST["copies"]
        copies_issued = 0

        books = Book.objects.create(name=name, author=author, isbn=isbn, category=category,
                                    rack_no=rack_no, copies=copies, copies_issued=copies_issued)
        books.save()
        alert = True
        return render(request, "add_book.html", {'alert': alert})
    return render(request, "add_book.html")

# @login_required(login_url = 'login/clerk_login/')
# def add_book(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         author = request.POST["author"]
#         isbn = request.POST["isbn"]
#         category = request.POST["category"]
#         rack_no = request.POST['rack_no']
#         copies = request.POST["copies"]
#         copies_issued = 0
#         reserve_id = None


#         copy = Book.objects.filter(name = name).first()
#         if copy==None:
#             book = Book.objects.create(name = name, author = author, isbn = isbn, category = category, rack_no = rack_no,
#                                         copies = copies, copies_issued = copies_issued, reserve_id = reserve_id)

#             book.save()
#         else:
#             book = Book.objects.get(name = name)
#             book.copies += 1

#         return render(request, "add_book.html",{'alert' : True})
#     return render(request, "add_book.html")


@login_required(login_url='/login')
def view_books(request):
    books = Book.objects.all()
    return render(request, "view_books.html", {'books': books})


@login_required(login_url='/login')
def delete_book(request, myid):
    books = Book.objects.filter(id=myid)
    books.delete()
    return redirect("/view_books")



def change_password(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "change_password.html", {'alert': alert})
            else:
                currpasswrong = True
                return render(request, "change_password.html", {'currpasswrong': currpasswrong})
        except:
            pass
    return render(request, "change_password.html")




# def list_books(request):
#     # books = Book.objects.all().values()
#     books = Book.objects.all()
#     return render(request, "list_books.html", {'books':books})

# def delete_book(request,isbn):
#     book = Book.objects.get(isbn = isbn)
#     book.delete()
#     return render(request,"list_books.html",{'alert':True})

@login_required(login_url='/login')
def edit_book(request, myid):
    # book = Book.objects.get(isbn = isbn)
    book = Book.objects.filter(id=myid).first()
    if request.method == "POST":
        book.name = request.POST["name"]
        book.author = request.POST["author"]
        book.isbn = request.POST["isbn"]
        book.category = request.POST["category"]
        book.rack_no = request.POST['rack_no']
        book.copies = request.POST["copies"]
        # book.copies_issued = request.POST["copies_issued"]
        # book.reserve_id = request.POST["reserve_ids"]
        # arr = request.POST["last_issue_id"]
        # book.set_last_issue_id(arr)
        # arr = request.POST["last_issue_date"]
        # book.set_last_issue_id(arr)
        book.save()
        return render(request, "edit_book.html", {'alert': True})
    return render(request, 'edit_book.html')

@login_required(login_url='/login')
def issue_book(request, isbn, insti_id):
    isbn = request.POST['isbn']
    insti_id = request.POST['insti_id']
    book = Book.objects.filter(isbn=isbn)
    user = Student.objects.get(insti_id=insti_id)
    if user == None:
        user = Faculty.objects.get(insti_id=insti_id)
    if book.copies == book.copies_issued:
        return render(request, 'view_books.html', {'alert': False})
    if (book.copies - book.copies_issued) == 1:
        if((ReservedBook.objects.filter(isbn = isbn) is not None) ):
            temp_book = ReservedBook.objects.get(isbn = isbn)
            if(((temp_book.available_date - datetime.date.today().isoforamt()).days < 7) and
                              (user.insti_id != insti_id) ):
                return render(request, 'view_books.html', {'alert': False})
                
    if book.copies > (book.copies_issued):

        
        no_books = len(IssuedBook.objects.filter(user_id = user.insti_id))
        if user.book_limit > no_books:
            insti_id = insti_id
            category = user.category
            isbn = isbn
            book_name = book.name
            issued_date = datetime.date.today().isoformat()
            expiry_date = datetime.date.today().isoformat() + datetime.timedelta(days = 30)

            issued_book = IssuedBook.objects.create(insti_id = insti_id, category = category, isbn = isbn, 
                                                    issued_date = issued_date, expiry_date = expiry_date,book_name = book_name)

            if ReservedBook.objects.filter(isbn = isbn) is not None:
                reserved_book = ReservedBook.objects.get(isbn = isbn)
                reserved_book.delete()
            return render(request, "view_books.html", {'alert': True})
        else:
            return render(request, "view_books.html", {'alert': False})
    else:
        return render(request, "view_books.html", {'alert': False})
  
@login_required(login_url='/login')
def reserve_book(request, isbn, insti_id):
    
    #if ReservedBook.objects.filter(isbn = isbn) is not None:
     #   return render(request, "view_books.html",{'alert':False})
    if request.method == "POST":
        isbn = request.POST['isbn']
        insti_id = request.POST['insti_id']
    book = Book.objects.get(isbn=isbn)
    user = Student.objects.get(insti_id=insti_id)
    if user == None:
        user = Faculty.objects.get(insti_id=insti_id)

    if (ReservedBook.objects.filter(insti_id = insti_id) or ReservedBook.objects.filter(isbn = isbn)) is not None:
        return render(request, "view_books.html",{'alert':False})
    else:
        insti_id = insti_id
        category = book.category
        isbn = isbn
        reserved_date = datetime.date.today().isoformat()

        reserve = ReservedBook.objects.create(insti_id = insti_id, category = category, isbn = isbn, reserved_date = reserved_date)

        return render(request, "view_books.html", {'alert': True})
    

@login_required(login_url='/login')
def return_book(request, isbn, insti_id):
    if request.method == "POST":
        isbn = request.POST['isbn']
        insti_id = request.POST['insti_id']
    
    issued_book = IssuedBook.objects.get(isbn = isbn)
    issued_book.delete()

    if ReservedBook.objects.filter(isbn = isbn) is not None:
        book = ReservedBook.objects.get(isbn = isbn)
        book.available_date = datetime.date.today().isoformat()
        
    return render(request, "view_books.html", {'alert': True})
