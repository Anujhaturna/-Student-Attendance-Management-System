from django import forms
from .models import Class, Section, Subject, ClassSubjectAssignment
from authentication.models import TeacherProfile


# Form for Adding a Class
class ClassForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.all(),
        required=False,  # Optional Class Teacher
        empty_label="Select Class Teacher (Optional)",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Class
        fields = ['name', 'teacher']
        widgets = {
            'name': forms.Select(choices=Class.CLASS_CHOICES, attrs={'class': 'form-control'}),
        }


# Form for Adding a Section
class SectionForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(
        queryset=TeacherProfile.objects.all(),
        required=False,  # Optional Section Teacher
        empty_label="Select Section Teacher (Optional)",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Section
        fields = ['class_name', 'section_name', 'teacher']
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'section_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., A, B, C'}),
        }


# Form for Adding a Subject
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subject Name'}),
        }


# Form for Assigning Teachers to Subjects in a Class-Section
class ClassSubjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ClassSubjectAssignment
        fields = ['class_name', 'section', 'subject', 'teacher']
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }
