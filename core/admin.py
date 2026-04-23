from django.contrib import admin

# Register your models here.

from .models import (Students,Classroom,ClassSubject,Subject,Teacher,TeacherClassSubject)

admin.site.register(Students)
admin.site.register(Classroom)
admin.site.register(ClassSubject)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(TeacherClassSubject)

