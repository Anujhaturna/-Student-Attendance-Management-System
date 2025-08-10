from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import student_register, teacher_register
from admin_panel import views as admin_views  # ✅ Admin Panel handles Admin & Principal dashboards
from teacher import views as teacher_views  # ✅ Teacher Panel
from student import views as student_views  # ✅ Student Panel

urlpatterns = [
    # ✅ User Authentication Routes
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="user_login"),  # ✅ Use "user_login" as name
    path("logout/", views.user_logout, name="user_logout"),

    # ✅ Password Reset Routes
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="authentication/password_reset.html"),
         name='password_reset'),
    path(
        "password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        "reset_done/",
        auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"),
        name="password_reset_complete",
    ),

    # ✅ Dashboard Routes
    path("admin-dashboard/", admin_views.admin_dashboard, name="admin_dashboard"),  # ✅ Admin Panel
    path("principal-dashboard/", admin_views.principal_dashboard, name="principal_dashboard"),
    # ✅ Principal handled in admin_panel
    path("teacher-dashboard/", teacher_views.teacher_dashboard, name="teacher_dashboard"),  # ✅ Teacher Panel
    path("student-dashboard/", student_views.student_dashboard, name="student_dashboard"),  # ✅ Student Panel

    # ✅ Registration Routes
    path('student-register/', student_register, name='student_register'),
    path('teacher-register/', teacher_register, name='teacher_register'),

]
