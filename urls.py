from django.urls import path
from .views import home, upload_image, user_login, user_logout,user_register

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_image, name='upload'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),    
    path('register/', user_register, name='register'),
]
