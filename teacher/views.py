import json

from django.views.decorators.csrf import csrf_exempt

from student.models import LeaveRequest

from .models import StudentProfile
from admin_panel.models import Section
from admin_panel.models import Class


def teacher_login(request):
    return render(request, 'teacher_login.html')


# Create your views here.
from datetime import datetime, timedelta

from authentication.forms import TeacherProfileForm

from django.contrib.auth.decorators import login_required
# ✅ Import fixed
from admin_panel.models import Section  # ✅ Ensure Section model is imported
from .models import Attendance

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import StudentProfile, Attendance
from datetime import date

import re
from django.shortcuts import render


def extract_number(text):
    match = re.search(r'\d+', text)  # Extract first number
    return int(match.group()) if match else float('inf')


def take_attendance(request):
    subjects = [
        "Marathi", "Hindi", "English", "Mathematics",
        "Science", "History", "Geography", "Physical Education"
    ]

    class_choices = sorted(
        set(Class.objects.values_list("name", flat=True)),
        key=extract_number  # Improved sorting
    )

    section_choices = sorted(set(Section.objects.values_list("section_name", flat=True)))

    return render(request, "teacher/take_attendance.html", {
        "subjects": subjects,
        "class_choices": class_choices,
        "section_choices": section_choices,
    })


# ✅ API to fetch students dynamically

from admin_panel.models import Class  # Import all required models

# Ensure correct import

from django.http import JsonResponse
from authentication.models import StudentProfile  # Adjust according to your model


def get_students(request):
    class_name = request.GET.get('class_name')
    section = request.GET.get('section')

    if class_name and section:
        students = StudentProfile.objects.filter(class_name=class_name, section=section)
        student_data = [{"id": s.id, "full_name": s.full_name, "roll_number": s.roll_number} for s in students]
        return JsonResponse({"students": student_data})

    return JsonResponse({"error": "Invalid request"}, status=400)


# ✅ API to submit attendance
from django.http import JsonResponse

from .models import StudentProfile, Attendance

from django.http import JsonResponse
from django.http import JsonResponse

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Attendance
from authentication.models import StudentProfile  # ✅ Import StudentProfile
from datetime import datetime


@csrf_exempt
def submit_attendance(request):
    """ Handle attendance submission """
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            attendance_records = data.get("attendance", [])
            section = data.get("section")
            subject = data.get("subject")
            attendance_date = data.get("attendance_date")

            # ✅ Validate input fields
            if not section or not subject or not attendance_date:
                return JsonResponse({"error": "Section, Subject, and Date are required."}, status=400)

            if not attendance_records:
                return JsonResponse({"error": "No attendance records submitted."}, status=400)

            for record in attendance_records:
                student_id = record.get("student_id")
                status = record.get("status")

                if not student_id or not status:
                    return JsonResponse({"error": "Missing student_id or status."}, status=400)

                student = get_object_or_404(StudentProfile, id=student_id)

                # ✅ Fix: Use `student.class_name` for `class_grade`
                Attendance.objects.create(
                    student=student,
                    class_grade=student.class_name,  # Fetch from StudentProfile
                    section=section,
                    subject=subject,
                    date=attendance_date,
                    status=status
                )

            return JsonResponse({"message": "Attendance submitted successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TeacherProfile

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeacherProfile
from .forms import TeacherProfileForm


@login_required(login_url='/authentication/login/')  # Ensure only logged-in users can access
def teacher_profile(request):
    teacher = get_object_or_404(TeacherProfile, user=request.user)

    if request.method == "POST":
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('teacher_profile')  # Redirect using the correct name from urls.py
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'teacher/teacher_profile.html', {'teacher': teacher, 'form': form})


def update_profile(request):
    teacher = get_object_or_404(TeacherProfile, user=request.user)
    if request.method == "POST":
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('teacher_profile')  # Redirect to the profile page
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'teacher/update_profile.html', {'form': form})


from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Attendance, StudentProfile

from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Attendance  # Ensure this import matches your project structure
# views.py
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Attendance

# views.py
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Attendance


def attendance_graph(request):
    labels_last_7_days, present_last_7_days, absent_last_7_days = [], [], []
    labels_monthly, present_monthly, absent_monthly = [], [], []
    today = timezone.now()

    class_filter = request.GET.get('class_grade')
    section_filter = request.GET.get('section')
    month_filter = request.GET.get('month')

    # Last 7 days attendance
    for i in range(7):
        date = today - timedelta(days=i)
        labels_last_7_days.append(date.strftime('%Y-%m-%d'))

        attendance_qs = Attendance.objects.filter(date=date)
        if class_filter:
            attendance_qs = attendance_qs.filter(class_grade=class_filter)
        if section_filter:
            attendance_qs = attendance_qs.filter(section=section_filter)

        present_last_7_days.append(attendance_qs.filter(status="Present").count())
        absent_last_7_days.append(attendance_qs.filter(status="Absent").count())

    # Monthly attendance
    if month_filter:
        year = today.year
        try:
            month = int(month_filter)
        except ValueError:
            return JsonResponse({'error': 'Invalid month'}, status=400)

        for day in range(1, 32):
            try:
                date = timezone.datetime(year, month, day)
                labels_monthly.append(date.strftime('%Y-%m-%d'))

                attendance_qs = Attendance.objects.filter(date=date)
                if class_filter:
                    attendance_qs = attendance_qs.filter(class_grade=class_filter)
                if section_filter:
                    attendance_qs = attendance_qs.filter(section=section_filter)

                present_monthly.append(attendance_qs.filter(status="Present").count())
                absent_monthly.append(attendance_qs.filter(status="Absent").count())
            except ValueError:
                break

    return JsonResponse({
        'labels_last_7_days': labels_last_7_days[::-1],
        'present_last_7_days': present_last_7_days[::-1],
        'absent_last_7_days': absent_last_7_days[::-1],
        'labels_monthly': labels_monthly,
        'present_monthly': present_monthly,
        'absent_monthly': absent_monthly
    })


def attendance_chart_view(request):
    return render(request, 'teacher/attendance_report.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from student.models import LeaveRequest

# Import Notification model


from django.shortcuts import render, get_object_or_404
from authentication.models import TeacherProfile
from student.models import LeaveRequest
from admin_panel.models import Notification


@login_required
def teacher_dashboard(request):
    teacher_profile = get_object_or_404(TeacherProfile, user=request.user)

    # Fetch ALL leave requests (Pending, Approved, Rejected)
    leave_requests = LeaveRequest.objects.filter(
        teacher=teacher_profile
    ).order_by('-start_date')  # Latest first

    notifications = Notification.objects.filter(recipient=request.user, is_read=False)

    return render(request, 'teacher/teacher_dashboard.html', {
        'teacher_profile': teacher_profile,
        'leave_requests': leave_requests,
        'notifications': notifications
    })

def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('teacher_dashboard')


from django.db.models import Q

from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import TeacherProfile, StudentProfile

from django.shortcuts import get_object_or_404
from django.contrib import messages

import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from admin_panel.models import Notification

logger = logging.getLogger(__name__)


def approve_leave(request, leave_id):
    if request.method == "POST":
        try:
            leave_request = get_object_or_404(LeaveRequest, id=leave_id)

            logger.info(f"🔄 Approving leave request ID: {leave_request.id}, Current status: {leave_request.status}")

            # ✅ Force update the status and save
            leave_request.status = "Approved"
            leave_request.save(update_fields=['status'])

            # ✅ Refresh from DB to verify changes
            leave_request.refresh_from_db()
            logger.info(f"✅ Leave request ID: {leave_request.id}, New status: {leave_request.status}")

            if leave_request.status != "Approved":
                logger.error(f"❌ Status update failed. Current DB value: {leave_request.status}")
                return JsonResponse({"success": False, "error": "Status update failed."}, status=500)

            # ✅ Create a notification for the student
            Notification.objects.create(
                recipient=leave_request.student.user,
                message=f"Your leave request from {leave_request.start_date} to {leave_request.end_date} has been approved.",
                is_read=False
            )

            return JsonResponse({"success": True})

        except Exception as e:
            logger.error(f"❌ Error approving leave: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


# Redirect to the pending leaves page

@login_required
def reject_leave(request, leave_id):
    if request.method == "POST":
        leave_request = get_object_or_404(LeaveRequest, id=leave_id)
        leave_request.status = "Rejected"
        leave_request.save()

        # Send notification to student
        Notification.objects.create(
            recipient=leave_request.student.user,
            message=f"Your leave request from {leave_request.start_date} to {leave_request.end_date} has been rejected."
        )

        return JsonResponse({"success": True})  # Return JSON response
    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


from django.shortcuts import render
from student.models import LeaveRequest  # Import your LeaveRequest model


def pending_leaves(request):
    # Fetch only pending leave requests
    leaves = LeaveRequest.objects.filter(status='Pending')
    return render(request, 'teacher/pending_leaves.html', {'leaves': leaves})


from django.shortcuts import render
from .models import Attendance


def view_attendance(request):
    attendances = Attendance.objects.all()
    return render(request, "teacher/attendance_list.html", {"attendances": attendances})


from django.shortcuts import render
from authentication.models import StudentProfile, TeacherProfile


def teacher_student_list(request):
    students = StudentProfile.objects.all()
    return render(request, 'teacher/teacher_student_list.html', {'students': students})


def teacher_teacher_list(request):
    teachers = TeacherProfile.objects.all()
    return render(request, 'teacher/teacher_teacher_list.html', {'teachers': teachers})


def teacher_view_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, 'teacher/teacher_view_student.html', {'student': student})


from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Attendance
from authentication.models import StudentProfile  # Ensure you have Attendance model

from django.shortcuts import render
from admin_panel.models import Class, Section, Subject

from django.shortcuts import render
from admin_panel.models import Class, Section, Subject


def attendance_report(request):
    classes = Class.objects.all()
    sections = Section.objects.all()
    subjects = Subject.objects.all()

    print("Classes:", classes)  # Debugging
    print("Sections:", sections)  # Debugging
    print("Subjects:", subjects)  # Debugging

    return render(request, "teacher/attendance_report.html", {
        "class_choices": classes,
        "section_choices": sections,
        "subjects": subjects,
    })


from django.http import JsonResponse
from django.utils.timezone import now
from datetime import timedelta
from .models import Attendance  # Your Attendance model (if it's in the same app)
from admin_panel.models import Class, Subject, Section  # Import models from admin_panel

from django.http import JsonResponse
from admin_panel.models import Class, Section, Subject


def get_classes(request):
    classes = list(Class.objects.values("id", "name"))
    return JsonResponse({"classes": classes})


def get_sections(request):
    sections = list(Section.objects.values("id", "section_name"))
    return JsonResponse({"sections": sections})


def get_subjects(request):
    subjects = list(Subject.objects.values("id", "name"))
    return JsonResponse({"subjects": subjects})


from .models import Attendance  # Ensure you have the correct model

from django.http import JsonResponse

from django.http import JsonResponse
from .models import Attendance  # Ensure you import the right model

from django.http import JsonResponse
from .models import Attendance
from django.http import JsonResponse
from teacher.models import Attendance
from django.http import JsonResponse
from .models import Attendance
from django.http import JsonResponse
from teacher.models import Attendance
from admin_panel.models import Class, Section, Subject

def get_attendance_report(request):
    time_range = request.GET.get("time_range")
    class_id = request.GET.get("class_id")
    section = request.GET.get("section_filter")  # ✅ Correct key
    subject_id = request.GET.get("subject_id")

    # 🔥 Fetch Class & Subject Names Dynamically
    class_name = Class.objects.filter(id=class_id).values_list("name", flat=True).first()
    subject = Subject.objects.filter(id=subject_id).values_list("name", flat=True).first()
    section_name = Section.objects.filter(id=section).values_list("section_name", flat=True).first()

    print(f"🔍 API Query → Class: {class_name}, Section: {section_name}, Subject: {subject}")

    # ✅ Build Query with Filters
    filters = {}
    if class_name:
        filters["class_grade__iexact"] = class_name
    if subject:
        filters["subject__iexact"] = subject
    if section_name:
        filters["section__iexact"] = section_name

    attendance_records = Attendance.objects.filter(**filters)

    # ✅ Debugging - Print Retrieved Data
    print("🎯 Retrieved Attendance:", list(attendance_records.values("class_grade", "section", "subject", "status")))

    present_count = attendance_records.filter(status__iexact="Present").count()
    absent_count = attendance_records.filter(status__iexact="Absent").count()

    print(f"🚀 Final API Counts → Present: {present_count}, Absent: {absent_count}")

    return JsonResponse({
        "present_count": present_count,
        "absent_count": absent_count,
        "debug_data": list(attendance_records.values("class_grade", "section", "subject", "status"))  # ✅ Debug data
    })



# views.py (Teacher app)
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def update_leave_status(request):
    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")
        message = request.POST.get("message", "")

        try:
            leave = LeaveRequest.objects.get(id=leave_id)
            if leave.teacher.user != request.user:
                return JsonResponse({"error": "Unauthorized"}, status=403)
            if action == "approve":
                leave.status = "Approved"
            elif action == "reject":
                leave.status = "Rejected"
            leave.response_message = message
            leave.save()
            return JsonResponse({"success": True, "status": leave.status})
        except LeaveRequest.DoesNotExist:
            return JsonResponse({"error": "Leave not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)
