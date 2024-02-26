# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import User
# from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
import json
import datetime


# class User(AbstractUser):
#     """User model."""

#     username = None
#     email = models.EmailField(_('email address'), unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []


# class Book(models.Model):
#     name = models.CharField(max_length=200)
#     author = models.CharField(max_length=200,blank = True)
#     isbn = models.CharField(max_length=20, blank = True)
#     category = models.CharField(max_length=50, blank=True)
#     rack_no = models.IntegerField(blank=True)
#     copies = models.IntegerField(blank=True)
#     copies_issued = models.IntegerField(blank=True)
#     # reserve_id = models.TextField(max_length=255, default=None)
#     # reserve_date = models.DateTimeField(default=datetime.now, blank=True)
#     # last_issue_id = models.TextField(default = None)
#     # last_issue_date = models.TextField(default = None)

#     def set_last_issue_id(self,arr):
#         self.last_issue_id = json.dumps(arr)


#     def get_last_issue_id(self):
#         return json.loads(self.last_issue_id)


#     def set_last_issue_date(self,arr):
#         self.last_issue_date = json.dumps(arr)

#     def get_last_issue_date(self):
#         return json.loads(self.last_issue_date)

#     def __str__(self):
#         return str(self.name) + " ["+str(self.isbn)+']'


# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     insti_id = models.CharField(max_length=10, blank=True)
#     department = models.CharField(max_length=10, blank=True)
#     category = models.CharField(max_length=10)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=10, blank=True)

#     def set_books_issued(self,arr):
#         self.books_issued= json.dumps(arr)


#     def get_books_issued(self):
#         return json.loads(self.books_issued)

#     def set_issued_date(self,arr):
#         self.issued_date = json.dumps(arr)

#     def get_issued_date(self,arr):
#         return json.loads(self.issued_date)

#     def __str__(self):
#         return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'

# class Faculty(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     insti_id = models.CharField(max_length=10, blank=True)
#     department = models.CharField(max_length=10, blank=True)
#     category = models.CharField(max_length=10)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=10, blank=True)

#     def set_books_issued(self,arr):
#         self.books_issued= json.dumps(arr)


#     def get_books_issued(self):
#         return json.loads(self.books_issued)

#     def set_issued_date(self,arr):
#         self.issued_date = json.dumps(arr)

#     def get_issued_date(self,arr):
#         return json.loads(self.issued_date)

#     def __str__(self):
#         return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'

# class Clerk(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     insti_id = models.CharField(max_length=10, blank=True)
#     category = models.CharField(max_length=10)
#     email = models.EmailField(max_length=50)
#     phone = models.CharField(max_length=10, blank=True)

#     def __str__(self):
#         return str(self.user) + " ["+str(self.insti_id)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'


# def expiry():
#     return datetime.today() + timedelta(days=30)


# class IssuedBook(models.Model):
#     student_id = models.CharField(max_length=1000, blank=True)
#     category = models.CharField(max_length=10, blank=True)
#     isbn = models.CharField(max_length=13)
#     issued_date = models.DateField(auto_now=True)
#     expiry_date = models.DateField(default=expiry)


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, insti_id, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not insti_id:
            raise ValueError('The given insti_id must be set')
        # email = self.normalize_email(email)
        user = self.model(insti_id=insti_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, insti_id, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(insti_id, password, **extra_fields)

    def create_superuser(self, insti_id, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(insti_id, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    insti_id = models.CharField(max_length=10, blank=True, unique=True)
    # first_name = models.CharField(max_length=50, blank=True)
    # last_name = models.CharField(max_length=50, blank=True)
    # department = models.CharField(max_length=10, blank=True)
    # category = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, unique=True)
    # phone = models.IntegerField(blank=True, unique=True, default= 0)
    otp = models.CharField(max_length=6)
    # email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'insti_id'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=10, blank=True)
    insti_id = models.CharField(max_length=10, blank=True, unique=True)
    category = models.CharField(max_length=10)
    phone = models.CharField(max_length=10, blank=True)
    fine = models.IntegerField(default=0)
    books_issued = models.IntegerField(default=0)
    # books_issued = models.TextField(default = None, blank=True)
    # issued_date = models.TextField(default=None,blank=True)
    book_limit = models.IntegerField(blank=True, default=0)


    def __str__(self):
        return str(self.user) + " ["+str(self.first_name)+" "+str(self.last_name)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=10, blank=True)
    insti_id = models.CharField(max_length=10, blank=True, unique=True)
    category = models.CharField(max_length=10)
    phone = models.CharField(max_length=10, blank=True)
    fine = models.IntegerField(default=0)

    # books_issued = models.TextField(default = None,null=True, blank=True)
    # issued_date = models.TextField(default=None,null=True, blank=True)
    books_issued = models.IntegerField(default=0)
    book_limit = models.IntegerField(blank=True, default=0)

   

    def __str__(self):
        return str(self.user) + " ["+str(self.first_name)+" "+ str(self.last_name)+']' + " ["+str(self.department)+']' + " ["+str(self.category)+']'


class Clerk(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    insti_id = models.CharField(max_length=50, blank=True, unique=True)
    phone = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return str(self.user) + " ["+str(self.first_name)+" "+ str(self.last_name)+']'


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    isbn = models.CharField(max_length=20, blank=True, unique=True)
    category = models.CharField(max_length=50, blank=True)
    rack_no = models.IntegerField(blank=True)
    copies = models.IntegerField(blank=True)
    copies_issued = models.IntegerField(default=0)
    # reserve_id = models.CharField(max_length=255, default=None)
    # reserve_date = models.DateTimeField(default=datetime.now, blank=True)
    # last_issue_id = models.TextField(default = None)
    # last_issue_date = models.TextField(default = None)

    def set_last_issue_id(self, arr):
        self.last_issue_id = json.dumps(arr)

    def get_last_issue_id(self):
        return json.loads(self.last_issue_id)

    def set_last_issue_date(self, arr):
        self.last_issue_date = json.dumps(arr)

    def get_last_issue_date(self):
        return json.loads(self.last_issue_date)

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'


def expiry():
    return datetime.today() + timedelta(days=30)


# class IssuedBook(models.Model):
#     student_id = models.CharField(max_length=1000, blank=True)
#     category = models.CharField(max_length=10, blank=True)
#     isbn = models.CharField(max_length=13)
#     issued_date = models.DateField(auto_now=True)
#     expiry_date = models.DateField(default=expiry)


class IssuedBook(models.Model):
    insti_id = models.CharField(max_length=200, blank=True)
    book_name = models.CharField(max_length=200, blank = True)
    author = models.CharField(max_length=200, blank=True)
    #user_id is the insit_id
    category = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return str(self.book_name) + " ["+str(self.isbn)+']'

class ReservedBook(models.Model):
    insti_id = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=255, blank = True)
    author = models.CharField(max_length = 255, blank = True)
    category = models.CharField(max_length=10, blank=True)
    isbn = models.CharField(max_length=13)
    reserved_date = models.DateField(auto_now=True)
    available_date = models.DateField(default=datetime.date.today)
    availability = models.BooleanField(default=False)
    #A user can reserve only one book and a book can be resered only by one user

    def __str__(self):
        return str(self.name) + " ["+str(self.isbn)+']'