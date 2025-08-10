from django.urls import path
from . import views  # Ensure views is imported



urlpatterns = [
    path("teacher-list/", views.teacher_list, name="teacher_list"),
    path("suspend-teacher/<int:teacher_id>/", views.suspend_teacher, name="suspend_teacher"),
    path("delete-teacher/<int:teacher_id>/", views.delete_teacher, name="delete_teacher"),
    path("send-announcement/", views.send_announcement, name="send_announcement"),
    path("notifications/", views.notification_list, name="notification_list"),
    path("student-list/", views.student_list, name="student_list"),
    path("student-detail/<int:student_id>/", views.student_detail, name="student_detail"),
]
