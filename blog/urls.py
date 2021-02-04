from django.urls import path
from . import views

app_name = 'blog'  # 视图函数命名空间
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/',
         views.ArchiveView.as_view(), name='archive'),
    path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('increase_likes/<int:id>/',
         views.PostLikesView.as_view(), name='increase_likes'),
    path('search/', views.search, name='search')
]
