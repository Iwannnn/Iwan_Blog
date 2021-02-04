from django.urls import path
from . import views

app_name = 'comments'
urlpatterns = [
    path('comment/<int:post_pk>', views.comment, name='comment'),
    path('comment/<int:post_pk>/<int:parent_comment_id>',
         views.comment, name='comment_reply')
]
