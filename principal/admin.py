from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Fields to display in the admin list view
    search_fields = ('title', 'message')  # Enables search functionality
    list_filter = ('created_at',)  # Adds filtering options

# OR (Alternative way)
# admin.site.register(Announcement, AnnouncementAdmin)
