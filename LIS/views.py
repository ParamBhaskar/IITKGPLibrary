from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from datetime import datetime, date,timedelta
import socket
from . import forms, models
import random
from django.conf import settings
import datetime
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
                
                if (Clerk.objects.filter(insti_id = request.user.insti_id).first() is None):
                    return redirect("/afterlogin")
                    
                else:
                    return redirect("/add_book")
        else:
            alert = True
            return render(request, "login.html", {'alert': alert})
    return render(request, "login.html")


def profile(request):
    books= Book.objects.all()
    iss= IssuedBook.objects.filter(insti_id= request.user.insti_id)
    user= Student.objects.filter(insti_id=request.user.insti_id).first()
    reserved_book = ReservedBook.objects.filter(insti_id = request.user.insti_id).first()

    if reserved_book is not None:
        if (reserved_book.available_date > datetime.date.today() ):
            reserved_book.availability = True
            reserved_book.save()
        else:
            reserved_book.availability = False
            reserved_book.save()

    if reserved_book is not None:
        print(reserved_book.name)
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()
    

    user.fine=0
    for book in iss:
        
        # day = book.expiry_date - book.issued_date
        day = datetime.date.today() - book.expiry_date
        print(day.days)
        # if day.days > 30:
        
        book.fine = (day.days)*1
        if book.fine>0:
            user.fine += book.fine
            print(book.fine)
            book.save()
            user.save()
        else:
            book.fine=0
            book.save()
            

    # print(user.phone)
    # print(user.department)
    request.phone = user.phone
    request.department=user.department
    request.category=user.category
    return render(request, "profile.html", {'iss': iss, 'books': books, 'res_book' : reserved_book})

@login_required(login_url='/login')
def afterlogin(request):
    return render(request, "afterlogin.html")


@login_required(login_url='/login')
def edit_profile(request):
    user = Student.objects.filter(insti_id=request.user.insti_id).first()
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()
    request.phone = user.phone
    request.department=user.department
    # student = Undergraduate.objects.get(user=request.user) or Postgraduate.objects.get(
    #     user=request.user) or ResearchScholar.objects.get(user=request.user)
    if request.method == "POST":
        email = request.POST['email']
        phone = request.POST['phone']
        department = request.POST['department']
        insti_id = request.POST['insti_id']

        # request.user.email = email
        # user.phone = phone
        # user.department = department
        # request.user.insti_id = insti_id
        # user.save()
        # request.user.save()
        request.user.email = email
        user.phone = phone
        user.department = department
        # user.insti_id = insti_id
        user.save()
        request.user.save()
        alert = True
        return render(request, "edit_profile.html", {'alert': alert})
    return render(request, "edit_profile.html")





@login_required(login_url='login/clerk_login/')
def view_issued_book(request):
    issuedBooks = IssuedBook.objects.all()
    # details = []
    # for i in issuedBooks:
    #     days = (date.today()-i.issued_date)
    #     d = days.days
    #     fine = 0
    #     if d > 30:
    #         day = d-30
    #         fine = day*1
    #     books = list(models.Book.objects.filter(isbn=i.isbn))
    #     students = list(models.Student.objects.filter(user=i.student_id))
    #     i = 0
    #     for l in books:
    #         t = (students[i].user, students[i].user_id, books[i].name, books[i].isbn,
    #              issuedBooks[0].issued_date, issuedBooks[0].expiry_date, fine)
    #         i = i+1
    #         details.append(t)
    return render(request, "view_issued_book.html", {'issuedBooks': issuedBooks})




def Logout(request):
    logout(request)
    return redirect("/")


@login_required(login_url='login/')
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
            u = User.objects.filter(id=request.user.id).first()
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


@login_required(login_url='/login')
def edit_book(request, myid):
    # book = Book.objects.get(id = myid)
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
    return render(request, "edit_book.html", {'book': book})


@login_required(login_url='/login')
def issue_book(request, myid):
    # isbn = request.POST['isbn']
    # insti_id = request.POST['insti_id']
    book = Book.objects.filter(id=myid).first()
    # user = Student.objects.get(insti_id=insti_id)
    user= Student.objects.filter(insti_id=request.user.insti_id).first()
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()
    if book.copies == book.copies_issued:
        return redirect('/profile/')
    if (book.copies - book.copies_issued) == 1:
        if((ReservedBook.objects.filter(isbn = book.isbn) is not None) ):
            temp_book = ReservedBook.objects.filter(id = myid).first()
            if temp_book != None:
               if(((temp_book.available_date - datetime.date.today().isoforamt()).days < 7) and
                              (user.insti_id != temp_book.insti_id) ):
                   return redirect('/profile/')
                #    return render(request, 'profile.html', {'alert2': True})
                
    if book.copies > (book.copies_issued):
        no_books = len(IssuedBook.objects.filter(insti_id = user.insti_id))
        # book.copies_issued=0
        # print(no_books)
        # print("Hi")
        # print(user.book_limit)
        if user.book_limit > no_books:
            book.copies_issued += 1
            book.save()
            insti_id = user.insti_id
            # category = book.category
            isbn = book.isbn
            book_name = book.name
            author=book.author
            issued_date = datetime.date.today()
            expiry_date = datetime.date.today() + timedelta(days = 30)
 
            issued_book = IssuedBook.objects.create(insti_id = insti_id, category = book.category, isbn = isbn, 
                                                    issued_date = issued_date, expiry_date = expiry_date,book_name = book_name,author=author)
            issued_book.save()

            if ReservedBook.objects.filter(isbn = book.isbn) is not None:
                reserved_book = ReservedBook.objects.filter(isbn = book.isbn)
                reserved_book.delete()
            # return render(request, "profile.html", {'alert': True})
            return redirect('/profile/')
        else:
            # return render(request, "profile.html", {'alert': False})
            return redirect('/profile/')
    else:
        return redirect('/profile/')
  
@login_required(login_url='/login')
def reserve_book(request, myid):
    
    #if ReservedBook.objects.filter(isbn = isbn) is not None:
     #   return render(request, "view_books.html",{'alert':False})
    print(1)
    book = Book.objects.filter(id = myid).first()
    user = Student.objects.filter(insti_id=request.user.insti_id).first()
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()

    if ((ReservedBook.objects.filter(insti_id = user.insti_id).first()) or (ReservedBook.objects.filter(isbn = book.isbn).first())) is not None:
        return redirect("/profile/")
    else:
        insti_id = user.insti_id
        category = book.category
        isbn = book.isbn
        reserved_date = datetime.date.today()

        reserve = ReservedBook.objects.create(insti_id = insti_id, category = category, isbn = isbn, reserved_date = reserved_date,name = book.name
                                              ,author = book.author)
        reserve.save()

        return redirect("/profile/")    

@login_required(login_url='/login')
def return_book(request, myid):
    issued_book = IssuedBook.objects.filter(id = myid).first()
    book = Book.objects.filter(isbn = issued_book.isbn).first()
    print(book.name)
    book.copies_issued -= 1
    book.save()
    user= Student.objects.filter(insti_id=request.user.insti_id).first()
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()

    
    # if request.method == "POST":
    #     isbn = request.POST['isbn']
    #     insti_id = request.POST['insti_id']
    
   
    user.fine -= issued_book.fine
    issued_book.delete()
    
    if ReservedBook.objects.filter(isbn = book.isbn).first() is not None:
        book = ReservedBook.objects.filter(isbn = book.isbn).first()
        book.available_date = datetime.date.today() + timedelta(days= 7)
        
    # return render(request, "profile.html", {'alert': True})
    return redirect("/profile/")



def contact(request):
    email=request.POST.get('email')
    name=request.POST.get('name')
    request.session['email']= request.POST['email']
    subject = "Hello from "+ name + " having Email ID: "+ email + " via Contact Form of LIS"
    message= request.POST.get('message')
    email_from= email
    email_to=["paramanandabhaskar@gmail.com"]
    message= EmailMessage(subject, message,email_from,email_to)
    message.send()

    # user = Student.objects.get(insti_id=request.user.insti_id)
    # if user == None:
    #     user = Faculty.objects.filter(insti_id=request.user.insti_id).first()
    if request.user.is_anonymous :
        return redirect('/')
    else:
        return redirect('/afterlogin/')

def payment(request):
    return render(request, "payment.html")

def bill(request):
    user = Student.objects.filter(user=request.user).first()
    iss= IssuedBook.objects.filter(insti_id= request.user.insti_id)
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()
    if user.fine==0:
        alert=True
        return render(request, "bill.html", {'alert': alert})
    else:
        total_fine=user.fine
        request.total_fine=total_fine
        return render(request, "bill.html",{'iss':iss,'total_fine':total_fine})
    
def reminder(request):

    user= Student.objects.filter(insti_id=request.user.insti_id).first()
    if user == None:
        user = Faculty.objects.filter(insti_id=request.user.insti_id).first()

    fine = ''
    issued = ''
    reserved = ''

    if user.fine > 0:
        fine = "Please clear your fine of rupees "+str(user.fine)
    else:
        fine = ''

    issued_book = IssuedBook.objects.filter(insti_id = request.user.insti_id).all()
    
    for book in issued_book:
        if book.expiry_date < datetime.date.today():
            issued += "Please return "+book.book_name+" as the issue is already expired\n"
    
    reserved_book = ReservedBook.objects.filter(insti_id = request.user.insti_id).first()

    if reserved_book is not None:
        if reserved_book.availability == True:
                print("hello")
                reserved = "Please issue your reserved book "+reserved_book.name+" before "+ str(reserved_book.available_date)

    request.fine=fine
    request.iss=issued
    request.res=reserved

    return render(request,"reminder.html")