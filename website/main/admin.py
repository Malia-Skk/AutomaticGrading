from django.contrib import admin
from .models import Question, Student

admin.site.site_header = 'Automatic Grading Admin'

# Register your models here.
admin.site.register(Question)
admin.site.register(Student)