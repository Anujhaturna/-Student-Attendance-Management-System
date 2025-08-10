from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.conf import settings
from .forms import CustomUserRegistrationForm, StudentProfileForm, TeacherProfileForm, StudentRegisterForm
from .models import CustomUser

User = get_user_model()


# ✅ User Registration
def register(request):
    if request.method == "POST":
        user_form = CustomUserRegistrationForm(request.POST)
        profile_form = None  # Initialize as None

        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False  # Requires admin approval
            user.save()

            # ✅ Choose the correct profile form based on user type
            if user.user_type == "student":
                profile_form = StudentProfileForm(request.POST)
            elif user.user_type == "teacher":  # Fix: Explicitly check for 'teacher'
                profile_form = TeacherProfileForm(request.POST)

            if profile_form and profile_form.is_valid():  # ✅ Ensure form exists
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

                try:
                    send_verification_email(request, user)
                    messages.success(request, "Please check your email to verify your account.")
                    return redirect("user_login")
                except Exception as e:
                    user.delete()
                    messages.error(request, f"Error sending email: {e}")
                    return redirect("register")

            user.delete()
            messages.error(request, "Profile form is invalid.")
        else:
            messages.error(request, "User form is invalid.")
    else:
        user_form = CustomUserRegistrationForm()
        profile_form = None  # Fix: Don't force StudentProfileForm initially

    return render(request, "authentication/register.html", {"user_form": user_form, "profile_form": profile_form})


# ✅ Email Verification
def send_verification_email(request, user):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = request.get_host()
    link = f"http://{domain}/verify/{uid}/{token}/"
    subject = "Verify your email"
    message = render_to_string("authentication/verify_email.html", {"link": link})

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return HttpResponse("Invalid verification link.")

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified. You can now log in.")
        return redirect("user_login")
    return HttpResponse("Invalid verification link.")


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            # Check if user is a teacher and suspended
            if hasattr(user, 'teacher_profile'):
                if user.teacher_profile.is_suspended:
                    messages.error(request, "Your account is suspended. Contact administration.")
                    return redirect("user_login")  # Redirect to login page

            login(request, user)
            return redirect(f"/authentication/{user.user_type}-dashboard/")  # ✅ Ensure correct URL

        messages.error(request, "Invalid username or password")

    return render(request, "authentication/login.html", {"form": AuthenticationForm()})

def user_logout(request):
    logout(request)
    return redirect("user_login")


# ✅ Student Registration with Email Notification to Admin
from admin_panel.models import Notification  # Ensure correct import
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import StudentRegisterForm, StudentProfileForm

# Ensure your User model is imported

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .forms import CustomUserRegistrationForm, StudentRegisterForm

from .models import CustomUser
from admin_panel.models import Notification
from .forms import CustomUserRegistrationForm, StudentRegisterForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserRegistrationForm, StudentRegisterForm
from .models import CustomUser, StudentProfile

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from authentication.models import StudentProfile
from authentication.forms import CustomUserRegistrationForm, StudentRegisterForm


def student_register(request):
    if request.method == "POST":
        user_form = CustomUserRegistrationForm(request.POST)
        student_form = StudentRegisterForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            try:
                # ✅ Create User Account
                user = user_form.save(commit=False)
                user.user_type = "student"
                user.is_active = False  # Awaiting Admin Approval
                user.set_password(user_form.cleaned_data["password1"])  # Hash password
                user.save()  # Explicitly saving user before using it in student profile

                # ✅ Create Student Profile
                student_profile = student_form.save(commit=False)
                student_profile.user = user  # Ensure user is saved before linking
                student_profile.save()

                # ✅ Send Email Notification to Admin (with error handling)
                admin_email = "himanshudongare143@gmail.com"  # Change to dynamic if needed
                try:
                    send_mail(
                        subject="🔔 New Student Registration Pending Approval",
                        message=f"A new student '{user.username}' has registered and needs approval.",
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[admin_email],
                        fail_silently=False,
                    )
                except Exception as email_error:
                    print(f"❌ Email Error: {email_error}")  # Debugging email issues

                messages.success(request, "Registration successful! Await admin approval.")
                return redirect("user_login")  # Redirect to login after registration

            except Exception as e:
                messages.error(request, f"Registration failed due to an error: {str(e)}")
                print(f"❌ Error: {e}")  # Debugging output

        else:
            # ❌ If form is invalid, log errors and show message
            messages.error(request, "There are errors in the form. Please correct them.")
            print("❌ Form Errors:", user_form.errors, student_form.errors)  # Debugging

    else:
        user_form = CustomUserRegistrationForm()
        student_form = StudentRegisterForm()

    return render(request, "authentication/student_register.html", {
        "user_form": user_form,
        "student_form": student_form,
    })


# ✅ Teacher Registration
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserRegistrationForm, TeacherProfileForm


# Ensure your User model is imported

def teacher_register(request):
    if request.method == "POST":
        user_form = CustomUserRegistrationForm(request.POST)
        profile_form = TeacherProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = "teacher"
            user.is_active = False  # Requires admin approval
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # ✅ Create a notification
            Notification.objects.create(
                message=f"New teacher '{user.username}' registered and needs approval.",
                is_read=False
            )

            # ✅ Send email notification to admin
            send_mail(
                "New Teacher Registration Pending Approval",
                f"A new teacher '{user.username}' has registered and needs approval.",
                settings.EMAIL_HOST_USER,
                ["himanshudongare143@gmail.com"],
                fail_silently=False,
            )

            messages.success(request, "Teacher registered successfully. Awaiting admin approval.")
            return redirect("user_login")

        else:
            print("Form Errors:", user_form.errors, profile_form.errors)  # Debugging

    return render(request, "authentication/teacher_register.html",
                  {"user_form": CustomUserRegistrationForm(), "profile_form": TeacherProfileForm()})


# ✅ Password Reset
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = request.build_absolute_uri(reverse("password_reset_confirm", args=[uid, token]))
                send_mail("Password Reset", f"Click to reset your password: {reset_link}", settings.EMAIL_HOST_USER,
                          [email])
            return render(request, "authentication/password_reset_done.html")
    return render(request, "authentication/password_reset_request.html", {"form": PasswordResetForm()})


# ✅ Send Approval Email
from django.core.mail import send_mail
from django.conf import settings


def send_approval_email(user, request):
    domain = request.get_host()  # Gets the IP and port
    login_url = f"http://{domain}/authentication/login/"

    subject = "Your Registration is Approved!"
    message = f"""
    Hello {user.username},

    Your account has been approved by the admin. You can now log in using your credentials.

    🔗 Login here: {login_url}

    Thank you!
    """
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
