from django import forms
from .models import CustomUser, StudentProfile, TeacherProfile


class CustomUserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ["username", "email", "user_type"]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Hash password
        if commit:
            user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['full_name', 'roll_number', 'class_name', 'section', 'date_of_birth', 'phone_number', 'address']


class TeacherProfileForm(forms.ModelForm):
    CLASS_CHOICES = [
        ("6th Grade", "6th Grade"),
        ("7th Grade", "7th Grade"),
        ("8th Grade", "8th Grade"),
        ("9th Grade", "9th Grade"),
        ("10th Grade", "10th Grade"),
        ("11th Grade", "11th Grade"),
        ("12th Grade", "12th Grade"),
    ]
    class_name = forms.ChoiceField(choices=CLASS_CHOICES, required=False)

    class Meta:
        model = TeacherProfile
        fields = ['full_name', 'subject', 'employee_id', 'phone_number', 'address', 'date_of_birth', 'qualifications',
                  'experience']

from django import forms
from django.contrib.auth.models import User  # Import User model

class StudentRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), required=True, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), required=True, label="Confirm Password")



    class Meta:
        model = StudentProfile
        fields = ['full_name', 'roll_number', 'class_name', 'section',
                  'date_of_birth', 'phone_number', 'address']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data
