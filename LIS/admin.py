from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Undergraduate)
admin.site.register(Postgraduate)
admin.site.register(ResearchScholar)
admin.site.register(Faculty)