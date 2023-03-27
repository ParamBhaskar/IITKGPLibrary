from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import json


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200,blank = True)
    isbn = models.CharField(max_length=20, blank = True)
    category = models.CharField(max_length=50, blank=True)
    rack_no = models.IntegerField(blank=True)
    copies = models.IntegerField(blank=True)
    copies_issued = models.IntegerField(blank=True)
    # reserve_id = models.TextField(max_length=255, default=None)
    # reserve_date = models.DateTimeField(default=datetime.now, blank=True)
    # last_issue_id = models.TextField(default = None)
    # last_issue_date = models.TextField(default = None)

    def set_last_issue_id(self,arr):
        self.last_issue_id = json.dumps(arr)


    def get_last_issue_id(self):
        return json.loads(self.last_issue_id)
    

    def set_last_issue_date(self,arr):
        self.last_issue_date = json.dumps(arr)

    def get_last_issue_date(self):
        return json.loads(self.last_issue_date)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def set_books_issued(self,arr):
        self.books_issued= json.dumps(arr)


    def get_books_issued(self):
        return json.loads(self.books_issued)

    def set_issued_date(self,arr):
        self.issued_date = json.dumps(arr)

    def get_issued_date(self,arr):
        return json.loads(self.issued_date)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def set_books_issued(self,arr):
        self.books_issued= json.dumps(arr)


    def get_books_issued(self):
        return json.loads(self.books_issued)

    def set_issued_date(self,arr):
        self.issued_date = json.dumps(arr)

    def get_issued_date(self,arr):
        return json.loads(self.issued_date)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'
    
class Clerk(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'


def expiry():
    return datetime.today() + timedelta(days=30)


class IssuedBook(models.Model):
    student_id = models.CharField(max_length=1000, blank=True)
    category = models.CharField(max_length=10, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
