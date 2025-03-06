from django.contrib.auth.views import LogoutView
from django.urls import path
from  . import views

app_name = "users"

urlpatterns = [
    path('user_home/', views.user_home, name='user_home'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
]