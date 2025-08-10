from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),  # Standardized logout path
    # Leave application form
    path('attendance/', views.view_attendance, name='view_attendance'),  # Attendance page
    path('success/', views.success, name='success'),  # Success page for form submissions
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path("list/", views.announcement_list, name="notification_list"),
    path('announcements/', views.announcement_list, name='announcement_list'),
]
