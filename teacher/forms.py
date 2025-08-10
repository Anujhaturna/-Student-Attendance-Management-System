from django import forms
from authentication.models import TeacherProfile


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        exclude = ["user"]  # Exclude user field (set automatically)
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make fields readonly
        readonly_fields = ["full_name", "employee_id", "date_of_birth"]
        for field in readonly_fields:
            self.fields[field].widget.attrs["readonly"] = True
            self.fields[field].widget.attrs["class"] = "readonly-field"

        # Email should be fetched from the user model
        self.fields["email"] = forms.EmailField(
            initial=self.instance.user.email if self.instance and self.instance.user else "",
            disabled=True,  # Prevent editing
            widget=forms.EmailInput(attrs={"class": "readonly-field"})
        )


from django import forms


class AttendanceForm(forms.Form):
    class_name = forms.CharField()
    section = forms.CharField()
    subject = forms.CharField()
    attendance_date = forms.DateField()
    status = forms.MultipleChoiceField(choices=[('Present', 'Present'), ('Absent', 'Absent')])
