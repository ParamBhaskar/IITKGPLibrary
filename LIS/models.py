from django.db import models
from django.contrib.postgres.fields.array import ArrayField
import psycopg2

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
    last_issue_id = ArrayField(models.CharField(max_length=255))
    last_issue_date = ArrayField(models.DateField(blank = True))

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

    def __str__(self):
        return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'
