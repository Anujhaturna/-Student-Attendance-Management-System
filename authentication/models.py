from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


# Custom Manager for CustomUser Model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('principal', 'Principal'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_approved = models.BooleanField(default=False)  # ✅ Admin Approval Required

    objects = CustomUserManager()  # Use Custom Manager

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


# Student Profile Model
class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile")
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=20)  # Example: "10th Grade"
    section = models.CharField(max_length=5)  # Example: "A"
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    remarks = models.TextField(blank=True, null=True)

    def leave_requests(self):
        return self.leaverequest_set.all()

    def __str__(self):
        return f"{self.full_name} - {self.roll_number}"

    class Meta:
        verbose_name = "Student Profile"
        verbose_name_plural = "Student Profiles"


# Teacher Profile Model
class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_profile")
    full_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    employee_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    qualifications = models.TextField()
    experience = models.IntegerField(help_text="Experience in years")
    class_name = models.CharField(max_length=50, null=True, blank=True)
    is_suspended = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.full_name} ({self.subject})"

    class Meta:
        verbose_name = "Teacher Profile"
        verbose_name_plural = "Teacher Profiles"
