from django.db import models
from django.contrib.auth import get_user_model
# ❌ Remove this from the top
from authentication.models import TeacherProfile, StudentProfile


# ✅ Import inside a function (Only when needed)
def some_function():
    from authentication.models import TeacherProfile
    # Now you can use TeacherProfile here


# Importing TeacherProfile for teacher assignment

User = get_user_model()


# Notification model for alerts
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
                                  blank=True)  # Admin who receives the notification
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when last updated
    is_read = models.BooleanField(default=False)  # Mark as read when clicked

    def __str__(self):
        if self.recipient:
            return f"Notification for {self.recipient.username}: {self.message[:50]}"
        return f"Notification: {self.message[:50]}"

    class Meta:
        ordering = ["-created_at"]  # Show latest notifications first


# Class model
class Class(models.Model):
    CLASS_CHOICES = [
        ('1st Grade', '1st Grade'),
        ('2nd Grade', '2nd Grade'),
        ('3rd Grade', '3rd Grade'),
        ('4th Grade', '4th Grade'),
        ('5th Grade', '5th Grade'),
        ('6th Grade', '6th Grade'),
        ('7th Grade', '7th Grade'),
        ('8th Grade', '8th Grade'),
        ('9th Grade', '9th Grade'),
        ('10th Grade', '10th Grade'),
    ]
    name = models.CharField(max_length=20, choices=CLASS_CHOICES, unique=True)  # Class name (e.g., "10th Grade")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="class_teacher")

    def __str__(self):
        return self.name


# Section model
class Section(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="sections")  # Related to Class
    section_name = models.CharField(max_length=10)  # Section name (e.g., "A", "B")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="section_teacher")

    def __str__(self):
        return f"{self.class_name} - {self.section_name}"


from django.db import models

from authentication.models import TeacherProfile  # Import the correct model

from authentication.models import TeacherProfile  # Correct import
from authentication.models import TeacherProfile  # Import from authentication


class Subject(models.Model):
    name = models.CharField(max_length=50, unique=True)
    assigned_teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.SET_NULL,  # If teacher is deleted, keep subject
        null=True,
        blank=True,
        related_name="subject_assignments"
    )

    def __str__(self):
        return self.name


# Assigning Teachers to Subjects in a Class-Section
class ClassSubjectAssignment(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="assigned_classes")  # Class
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="assigned_sections")  # Section
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assigned_subjects")  # Subject
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE,
                                related_name="assigned_teachers")  # Assigned Teacher

    def __str__(self):
        return f"{self.class_name} - {self.section} | {self.subject} -> {self.teacher.user.username}"


class Remark(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    remark = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Remark for {self.student.full_name}"
