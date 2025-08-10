from django.contrib import admin
from .models import LeaveRequest


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'start_date', 'end_date', 'teacher')  # Filter by status, date, teacher
    search_fields = ('student__full_name', 'teacher__full_name', 'reason')  # Search functionality
    ordering = ('-created_at',)  # Orders newest requests first
    list_editable = ('status',)  # Allows inline status change in the admin panel

# Alternative way:
# admin.site.register(LeaveRequest, LeaveRequestAdmin)
