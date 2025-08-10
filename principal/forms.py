from django import forms
from authentication.models import CustomUser
from admin_panel.models import Notification


class NotificationForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(queryset=CustomUser.objects.filter(user_type="student"))

    class Meta:
        model = Notification
        fields = ['message', 'recipient']  # ✅ Removed 'title' since it's not in the model


from django import forms
from .models import Announcement


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ["title", "message"]  # Fields to be filled in the form
