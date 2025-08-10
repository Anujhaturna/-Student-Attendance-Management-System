from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, get_user_model, authenticate, login
from authentication.models import TeacherProfile, StudentProfile, CustomUser
from .models import Notification  # Ensure Notification model exists
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()


# ✅ Admin Login
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:  # Ensuring only admins can log in
            login(request, user)
            return redirect("admin_dashboard")  # Redirect to admin panel
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, "admin_panel/login.html")


# ✅ Approve & Reject Users
def approve_user(request):
    query = request.GET.get("search", "").strip()
    role_filter = request.GET.get("role", "all")

    users = CustomUser.objects.filter(is_approved=False)  # Ensure filtering pending users correctly

    if query:
        users = users.filter(Q(username__icontains=query) | Q(email__icontains=query))

    if role_filter == "teacher":
        users = users.filter(user_type="teacher")
    elif role_filter == "student":
        users = users.filter(user_type="student")

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        action = request.POST.get("action")
        user = get_object_or_404(CustomUser, id=user_id)

        if action == "approve":
            user.is_approved = True
            user.is_active = True  # Activate account
            user.save()

            Notification.objects.create(
                message=f"✅ {user.username} has been approved!",
                is_read=False,
                recipient=user
            )

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "admin_notifications",
                {
                    "type": "send_notification",
                    "message": f"✅ {user.username} has been approved!",
                },
            )

            login_url = f"http://{request.get_host()}/authentication/login/"
            send_mail(
                'Your Registration is Approved!',
                f'Hello {user.username},\n\nYour account has been approved. You can now log in here: {login_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, f"{user.username} has been approved.")

        elif action == "reject":
            user.delete()
            messages.error(request, f"{user.username} has been rejected.")

        return redirect("authentication:approve_user")

    return render(request, "admin_panel/approve_users.html", {"pending_users": users})


# ✅ Admin Dashboard with Notifications

from django.shortcuts import render
from authentication.models import CustomUser  # Ensure this matches your user model
from django.shortcuts import render
from authentication.models import CustomUser
from admin_panel.models import Notification


def admin_dashboard(request):
    notifications = []
    unread_count = 0

    # Fetch only users who are pending approval
    pending_users = CustomUser.objects.filter(is_approved=False).order_by(
        '-date_joined')  # Ensure this filters correctly

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
        unread_count = notifications.count()

    return render(request, 'admin_panel/dashboard.html', {
        'notifications': notifications,
        'unread_count': unread_count,
        'pending_users': pending_users,  # Only pending users
    })


# ✅ Mark Notification as Read
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('admin_dashboard')


# ✅ Send Notification to Admin When New User Registers
def create_user_notification(user):
    admins = User.objects.filter(is_superuser=True)  # Get all admins
    for admin in admins:
        Notification.objects.create(
            recipient=admin,
            message=f"New user {user.username} is pending approval."
        )


def manage_classes(request):
    """Handles class management, including adding new classes"""
    class_choices = [choice[0] for choice in Class.CLASS_CHOICES]  # Extract class names
    teachers = TeacherProfile.objects.all()  # Fetch all teachers
    classes = Class.objects.all()  # Fetch all existing classes
    sections = Section.objects.all()  # Fetch all existing sections

    if request.method == "POST":
        name = request.POST.get("class_name")  # Ensure correct field
        teacher_id = request.POST.get("teacher")

        if name in class_choices:  # Validate against predefined choices
            teacher = None
            if teacher_id:
                try:
                    teacher = TeacherProfile.objects.get(id=teacher_id)
                except TeacherProfile.DoesNotExist:
                    messages.error(request, "Selected teacher does not exist.")
                    return redirect("manage_classes")

            # Use correct field "name" instead of "class_name"
            class_obj, created = Class.objects.get_or_create(name=name, defaults={'teacher': teacher})
            if created:
                messages.success(request, "Class added successfully!")
            else:
                messages.warning(request, "This class already exists.")

        else:
            messages.error(request, "Invalid class name! Please select from the list.")

        return redirect("manage_classes")

    return render(request, "admin_panel/manage_classes.html",
                  {"classes": classes, "class_choices": class_choices, "teachers": teachers, "sections": sections})


def add_class(request):
    """Handles adding a new class"""
    class_choices = [choice[0] for choice in Class.CLASS_CHOICES]  # Extract class names

    if request.method == "POST":
        class_name = request.POST.get("class_name")
        teacher_id = request.POST.get("teacher")

        if class_name in class_choices:  # Validate against predefined choices
            teacher = None
            if teacher_id:
                try:
                    teacher = TeacherProfile.objects.get(id=teacher_id)
                except TeacherProfile.DoesNotExist:
                    messages.error(request, "Selected teacher does not exist.")
                    return redirect("manage_classes")

            # Use "name" field instead of "class_name"
            Class.objects.create(name=class_name, teacher=teacher)
            messages.success(request, "Class added successfully!")
        else:
            messages.error(request, "Invalid class name! Please select from the list.")

    return redirect("manage_classes")


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Class, Section
from authentication.models import TeacherProfile

from django.http import JsonResponse


def add_section(request):
    if request.method == "POST":
        class_id = request.POST.get("class_id")
        section_name = request.POST.get("section_name")
        section_teacher_id = request.POST.get("section_teacher")

        if not class_id or not section_name:
            return JsonResponse({"success": False, "error": "Missing required fields!"}, status=400)

        try:
            class_instance = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return JsonResponse({"success": False, "error": "Class not found!"}, status=400)

        teacher_instance = None
        if section_teacher_id:
            try:
                teacher_instance = TeacherProfile.objects.get(id=section_teacher_id)
            except TeacherProfile.DoesNotExist:
                return JsonResponse({"success": False, "error": "Teacher not found!"}, status=400)

        section = Section.objects.create(class_name=class_instance, section_name=section_name, teacher=teacher_instance)

        return JsonResponse({"success": True, "message": "Section added successfully!"})

    return JsonResponse({"success": False, "error": "Invalid request method!"}, status=400)


# ✅ Admin Logout
def admin_logout(request):
    logout(request)
    return redirect('home')


# ✅ Role-Based Dashboards
def teacher_dashboard(request):
    return render(request, "teacher/dashboard.html")


def student_dashboard(request):
    return render(request, "student/dashboard.html")


def principal_dashboard(request):
    return render(request, "principal/dashboard.html")


# ✅ Approved Users List
def approved_users_list(request):
    approved_users = CustomUser.objects.filter(is_active=True)  # Fetch only approved users
    return render(request, 'admin_panel/approved_users.html', {'approved_users': approved_users})


# ✅ Student & Teacher Lists
from django.contrib.auth.decorators import user_passes_test


# Function to check if the user is an admin


# Redirect teachers to their dashboard
def student_list(request):
    students = StudentProfile.objects.filter(user__is_active=True)  # Only approved students
    return render(request, 'admin_panel/student_list.html', {'students': students})


# Redirect teachers to their dashboard
def teacher_list(request):
    teachers = TeacherProfile.objects.filter(user__is_active=True).select_related("user")  # Only approved teachers
    return render(request, 'admin_panel/teacher_list.html', {'teachers': teachers})  # Fixed key name


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Class, Section


@csrf_exempt
def delete_class(request, class_id):
    try:
        class_obj = Class.objects.get(id=class_id)
        class_obj.delete()
        return JsonResponse({"success": True})
    except Class.DoesNotExist:
        return JsonResponse({"success": False, "error": "Class not found"})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Section

def delete_section(request, section_id):
    if request.method == "POST":
        section = get_object_or_404(Section, id=section_id)
        section.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from authentication.models import StudentProfile
from .models import Remark

from django.shortcuts import render


# Import StudentProfile model

def admin_student_list(request):
    students = StudentProfile.objects.all()  # Fetch all students
    return render(request, 'admin_panel/admin_student_list.html', {'students': students})


def admin_view_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    return render(request, 'admin_panel/admin_view_student.html', {'student': student})


def admin_edit_student(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    if request.method == "POST":
        student.full_name = request.POST.get('full_name')
        student.phone_number = request.POST.get('phone_number')
        student.address = request.POST.get('address')
        student.save()
        messages.success(request, "Student details updated successfully.")
        return redirect('admin_student_list')
    return render(request, 'admin_panel/admin_edit_student.html', {'student': student})


def admin_add_remark(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        remark_text = request.POST.get("remark")
        student = get_object_or_404(StudentProfile, id=student_id)
        Remark.objects.create(student=student, remark=remark_text)
        messages.success(request, "Remark added successfully.")
        return redirect('admin_student_list')


from django.shortcuts import render
from authentication.models import TeacherProfile  # Adjust import if needed


def admin_teacher_list(request):
    teachers = TeacherProfile.objects.filter(user__is_active=True)  # ✅ Only show active teachers
    return render(request, 'admin_panel/admin_teacher_list.html', {'teachers': teachers})


from django.shortcuts import get_object_or_404, redirect
from authentication.models import TeacherProfile  # Adjust import based on your model
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from authentication.models import TeacherProfile  # Adjust if needed
from django.shortcuts import get_object_or_404, redirect
from authentication.models import TeacherProfile
from django.contrib.auth.models import User


def suspend_teacher(request, teacher_id):
    teacher = get_object_or_404(TeacherProfile, id=teacher_id)

    # Ensure user instance is correctly updated
    user = teacher.user
    user.is_active = False  # ❗ Suspend the teacher
    user.save()  # ✅ Save the change

    return redirect('authentication:admin_teacher_list')  # ✅ Redirect to teacher list

# Redirect to the teacher list page
