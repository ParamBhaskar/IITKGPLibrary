from django.db import models
from django.contrib.postgres.fields.array import ArrayField
import json

# Create your models here.
from django.contrib.auth.models import User


class Book(models.Model):
    book_name = models.CharField(max_length=200)
    author = models.CharField(max_length=200,blank = True)
    isbn = models.CharField(blank = True)
    category = models.CharField(max_length=50, blank=True)
    rack_no = models.IntegerField(blank=True)
    copies = models.IntegerField(blank=True)
    copies_issued = models.IntegerField(blank=True)
    reserve_id = models.CharField(max_length=255)
    reserve_date = models.DateField(blank = True)
    last_issue_id = models.TextField(default = None)
    last_issue_date = models.TextField(default = None)

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


class Undergraduate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'
    
class Postgraduate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'
    
class ResearchScholar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=10, blank=True)
    department = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=10, blank=True)
    books_issued = models.TextField(defualt = None)
    issued_date = models.TextField(default=None)

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
