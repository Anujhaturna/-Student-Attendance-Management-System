from django.db import models
from django.utils.timezone import now
from authentication.models import StudentProfile, TeacherProfile  # ✅ Corrected import


class Attendance(models.Model):
    CLASS_CHOICES = [(str(i), f"Class {i}") for i in range(1, 11)]  # Classes 1-10
    SECTION_CHOICES = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')]  # Sections A-D
    SUBJECT_CHOICES = [
        ('Marathi', 'Marathi'),
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Mathematics', 'Mathematics'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Geography', 'Geography'),
        ('Physical Education', 'Physical Education'),
    ]
    STATUS_CHOICES = [('Present', 'Present'), ('Absent', 'Absent')]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="attendance_records")
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="marked_attendance")
    class_grade = models.CharField(max_length=10)  # ✅ Class (1-10)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)  # ✅ Section (A-D)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)  # ✅ Predefined subjects
    date = models.DateField(default=now)  # ✅ Default to today
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)  # ✅ Attendance status

    def __str__(self):
        return f"{self.student.user.first_name} - {self.class_grade}{self.section} - {self.subject} - {self.date} - {self.status}"
