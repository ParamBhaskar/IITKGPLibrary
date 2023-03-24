from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.PositiveIntegerField()
    category = models.CharField(max_length=50)

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
