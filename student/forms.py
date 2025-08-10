from django import forms
from authentication.models import StudentProfile, TeacherProfile
from student.models import LeaveRequest


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'roll_number', 'class_name', 'section', 'date_of_birth', 'phone_number', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['student', 'teacher', 'reason', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
