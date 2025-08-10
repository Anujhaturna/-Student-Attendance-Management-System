from django.urls import path
from . import views  # Import views from the same app
from .views import update_leave_status


urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('login/', views.teacher_login, name='teacher_login'),
    path('teacher_profile/', views.teacher_profile, name='teacher_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('take_attendance/', views.take_attendance, name='take_attendance'),
    path('attendance_chart/', views.attendance_chart_view, name='attendance_chart'),
    path('attendance_graph/', views.attendance_graph, name='attendance_graph'),
    path('notifications/read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path("approve-leave/<int:leave_id>/", views.approve_leave, name="approve_leave"),
    path("reject-leave/<int:leave_id>/", views.reject_leave, name="reject_leave"),
    path('pending-leaves/', views.pending_leaves, name='pending_leaves'),
    path("", views.take_attendance, name="mark_attendance"),
    path("get-students/", views.get_students, name="get_students"),
    path('submit_attendance/', views.submit_attendance, name='submit_attendance'),
    # API for student filtering
    path("attendance/", views.view_attendance, name="view_attendance"),
path('students/', views.teacher_student_list, name='teacher_student_list'),
    path('teachers/', views.teacher_teacher_list, name='teacher_teacher_list'),
    path('students/<int:student_id>/', views.teacher_view_student, name='teacher_view_student'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    path('get-attendance-report/', views.get_attendance_report, name='get_attendance_report'),
    path("get-subjects/", views.get_subjects, name="get_subjects"),
    path("get-classes/", views.get_classes, name="get_classes"),  # ✅ Add this
    path("get-sections/", views.get_sections, name="get_sections"),
    path("update-leave-status/", update_leave_status, name="update_leave_status"),

]
