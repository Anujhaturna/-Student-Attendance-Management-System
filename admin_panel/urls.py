from django.urls import path
from . import views
from .views import admin_dashboard, teacher_dashboard, student_dashboard, principal_dashboard
from authentication.views import user_logout
from .views import admin_student_list, admin_view_student, admin_edit_student, admin_add_remark

app_name = 'authentication'
urlpatterns = [
    # ✅ Admin Panel Routes
    path("dashboard/admin/", admin_dashboard, name="admin_dashboard"),  # ⬅ Clearer URL
    path('approve-users/', views.approve_user, name='approve_user'),
    # ✅ Approval page
    path("manage-classes/", views.manage_classes, name="manage_classes"),  # ✅ Manage Classes
    path("login/", views.admin_login, name="admin_login"),  # ✅ Admin Login

    # ✅ Role-Based Dashboards
    path("dashboard/teacher/", teacher_dashboard, name="teacher_dashboard"),
    path("dashboard/student/", student_dashboard, name="student_dashboard"),
    path("dashboard/principal/", principal_dashboard, name="principal_dashboard"),
    # Import the logout view
    path('approved-users/', views.approved_users_list, name='approved_users_list'),
    path('mark-as-read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('logout/', user_logout, name='logout'),
    # path('students/', views.student_list, name='student_list'),
    # path('teachers/', views.teacher_list, name='teacher_list'),
    path('add-class/', views.add_class, name='add_class'),
    path('add-section/', views.add_section, name='add_section'),
    path('students/', admin_student_list, name='admin_student_list'),
    path('admin/students/<int:student_id>/', admin_view_student, name='admin_view_student'),
    path('admin/students/<int:student_id>/edit/', admin_edit_student, name='admin_edit_student'),
    path('students/<int:student_id>/add-remark/', admin_add_remark, name='admin_add_remark'),

    # Other admin URLs...
    path('teachers/<int:teacher_id>/suspend/', views.suspend_teacher, name='admin_suspend_teacher'),
    path('teachers/', views.admin_teacher_list, name='admin_teacher_list'),
    path('delete_section/<int:section_id>/', views.delete_section, name='delete_section'),
]
