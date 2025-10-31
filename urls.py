from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from straw_management import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),  # Fix login path
    path('straw_management/', include('straw_management.urls')),  # Include app URLs
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)