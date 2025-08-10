from django.contrib import admin
from .models import Notification, Subject


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("recipient", "message", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("message", "recipient__username")


from django.contrib import admin
from .models import Class, Section  # Replace with actual model names


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ("name",)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section_name', 'teacher')


from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "assigned_teacher")  # Show these columns in admin
    search_fields = ("name", "assigned_teacher__user__full_name")  # Enable search
    list_filter = ("assigned_teacher",)  # Add filter on the right


from django.contrib import admin
from .models import ClassSubjectAssignment, Remark


@admin.register(ClassSubjectAssignment)
class ClassSubjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ("class_name", "section", "subject", "teacher")  # Columns in admin table
    search_fields = ("class_name__name", "section__name", "subject__name", "teacher__full_name")  # Search
    list_filter = ("class_name", "section", "subject")  # Filters on the right


@admin.register(Remark)
class RemarkAdmin(admin.ModelAdmin):
    list_display = ("student", "remark", "created_at")
    search_fields = ("student__full_name", "remark")
    list_filter = ("created_at",)
