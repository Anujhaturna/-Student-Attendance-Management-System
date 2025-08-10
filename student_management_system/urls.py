from django.contrib import admin
from django.urls import path, include
from .views import home  # ✅ Make sure `home` exists in `views.py`

urlpatterns = [
    path('', home, name='home'),
    path('student/', include('student.urls')),  # ✅ Student URLs
    path('teacher/', include('teacher.urls')),  # ✅ Teacher URLs
    path('admin/', include('admin_panel.urls')),
    path('authentication/', include('authentication.urls')),  # ✅ Admin Panel URLs
    path('principal/', include('principal.urls')),
    path('superadmin/', admin.site.urls),  # ✅ Default Django Admin
]
