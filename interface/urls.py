from django.urls import path
from . import views

app_name = 'interface'  # 视图函数命名空间
urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('about/', views.about, name='about'),
]
