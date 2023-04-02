# from django.contrib import admin
from .models import *

# # Register your models here.

# admin.site.register(Book)
# admin.site.register(Student)
# admin.site.register(Faculty)
# admin.site.register(IssuedBook)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('insti_id','email', 'password', 'otp')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('insti_id','email','password1', 'password2'),
        }),
    )
    list_display = ('insti_id', 'first_name', 'last_name','email', 'is_staff')
    search_fields = ('insti_id','email', 'first_name', 'last_name')
    ordering = ('insti_id',)



admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Clerk)
admin.site.register(IssuedBook)