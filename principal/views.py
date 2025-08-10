from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from authentication.models import TeacherProfile
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render
from authentication.models import TeacherProfile


@login_required
def teacher_list(request):
    teachers = TeacherProfile.objects.all()  # ✅ Fetch all teachers
    return render(request, "principal/teacher_list.html", {"teachers": teachers})


@login_required
def suspend_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)
    teacher.user.is_active = False  # Suspend the user
    teacher.user.save()
    messages.success(request, f"{teacher.full_name} has been suspended.")
    return redirect("teacher_list")


@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)
    teacher.user.delete()  # Delete the user
    messages.success(request, f"{teacher.full_name} has been deleted.")
    return redirect("teacher_list")


from django.shortcuts import render, redirect
from .forms import NotificationForm
from admin_panel.models import Notification

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AnnouncementForm  # Ensure you have this form
from .models import Announcement  # Ensure you have this model


def send_announcement(request):
    if request.method == "POST":
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Announcement sent successfully!")
            return redirect("send_announcement")  # Redirect to the same page after submission
    else:
        form = AnnouncementForm()

    return render(request, "principal/send_announcement.html", {"form": form})


def notification_list(request):
    notifications = Notification.objects.all().order_by("-created_at")
    return render(request, "principal/notification_list.html", {"notifications": notifications})


from django.shortcuts import render, get_object_or_404
from authentication.models import StudentProfile


def student_list(request):
    students = StudentProfile.objects.all()
    return render(request, "principal/student_list.html", {"students": students})


def student_detail(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, "principal/student_detail.html", {"student": student})
