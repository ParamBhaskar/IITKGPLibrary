from django.shortcuts import redirect, render, HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponse
import datetime

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

def add_book(request):
    if request.method == "POST":
        book_name = request.POST["book_name"]
        author = request.POST["author"]
        isbn = request.POST["isbn"]
        category = request.POST["category"]
        rack_no = request.POST['rack_no']
        copies = request.POST["copies"]
        copies_issued = 0
        reserve_id = []
        last_issue_id = []
        last_issue_date = []

        
        copy = Book.objects.filter(book_name = book_name)
        if copy==None:
            book = Book.objects.create(book_name = book_name, author = author, isbn = isbn, category = category, rack_no = rack_no,
                                        copies = copies, copies_issued = copies_issued, reserve_ids  = reserve_ids, last_issue = last_issue)

            book.save()
        else:
            book = Book.objects.get(book_name = book_name)
            book.copies += 1

        return render(request, "add_book.html",{'alert' : True})
    return render(request, "registration.html")

def list_books(request):
    books = Book.objects.all().values()
    context = {
        'books' : books,
    }
    return render(request, "list_books.html",{'alert':True})

def delete_book(request,isbn):
    book = Book.objects.get(isbn = isbn)
    book.delete()
    return render(request,"list_books.html",{'alert':True})


def edit_book(request,isbn):
    book = Book.objects.get(isbn = isbn)
    if request.method == "POST":
        book.book_name = request.POST["book_name"]
        book.author = request.POST["author"]
        book.isbn = request.POST["isbn"]
        book.category = request.POST["category"]
        book.rack_no = request.POST['rack_no']
        book.copies = request.POST["copies"]
        book.copies_issued = request.POST["copies_issued"]
        book.reserve_id = request.POST["reserve_ids"]
        book.last_issue_date = request.POST["last_issue"]
        book.last_issue_id = request.POST["last_issue"]
        book.save()
        return render(request, "list_books.html",{'alert':True})
    return render(request, 'list_books.html')

def issue_book(request,isbn,insti_id):
    book = Book.objects.get(isbn = isbn)
    if book.copies == book.copies_issued:
        book.save()
        return render(request, 'list_books.html',{'alert':False})
    
    if book.copies > book.copies_issued:
        
        user = Student.objects.get(insti_id = insti_id)
        if user == None:
            user = Faculty.objects.get(insti_id = insti_id)
        issued_books = len(user.book_issued)
        if user.book_limit > issued_books:
            user.books_issued.append(book)
            user.issued_date.append(datetime.date.today().isoformat())
            book.last_issue_id.append(insti_id)
            book.last_issue_date.append(datetime.date.today().isoformat())
        
        if user.reserved_book == isbn:
            user.reserved_book = None
            user.reserve_date = None
            book.reserve_id = None
            book.reserve_date = None
        book.save()
        user.save()
        return render(request,"list_books.html",{'alert': True})
    else:
        return render(request, "list_books.html",{'alert': False})
    
def reserve_book(request,isbn,insti_id):

    book = Book.objects.get(isbn = isbn)
    if(insti_id in book.last_issue_id):
        book.save()
        return render(request,"list_books.html",{'alert':False})

    user = Student.objects.get(insti_id = insti_id)
    if user == None:
        user = Faculty.objects.get(insti_id = insti_id)
    
    
    if book.copies == book.copies_issued:
        if book.reserve_id is not None:
            if isbn == user.reserved_book:
                return render(request,"list_books.html",{'alert':False})
            else:
                return render(request, "list_books.html",{'alert': False})
        

        else:
            user.reserved_book = isbn
            user.reserved_date = datetime.datetime.now()
            book.reserve_id = insti_id
            book.reserve_date = datetime.datetime.now()
            user.save()
            book.save()
            return render(request, 'list_books.html',{'alert':True}) 
    
def return_book(request,isbn,id):

    book = Book.objects.get(isbn = isbn)
    user = Student.objects.get(insti_id = id)
    if user == None:
        user = Faculty.objects.get(insti_id = id)

    if isbn not in user.books_issued:
        user.save()
        book.save()
        return render(request,"list_books.html",{'alert': False})
    book.copies_issued -=1
    index = book.last_issue_id.index(id)
    book.last_issue_id.pop(index)
    book.last_issue_date.pop(index)
    
    
    index = user.books_issued.index(isbn)
    user.books_issued.pop(index)
    user.issued_date.pop(index)
    book.save()
    user.save()
