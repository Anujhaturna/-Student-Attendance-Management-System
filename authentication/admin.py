from django.contrib import admin
from .models import CustomUser, StudentProfile, TeacherProfile

admin.site.register(CustomUser)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
