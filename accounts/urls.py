from django.urls import path
from . import views
from django.contrib import admin

app_name = "accounts"
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('edit/<int:id>/', views.profile_edit, name='edit'),
]
