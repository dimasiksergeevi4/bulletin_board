from django.urls import path
from .views import *

urlpatterns = [
   path('<int:pk>/', OnePost.as_view(), name='one_post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>/create/', CommentCreate.as_view(), name='comment_create'),
   path('comment/<int:pk>/approve/', approve_comment, name='comment_approve'),
   path('comment/<int:pk>/delete/', CommentDelete.as_view(), name='comment_delete'),
]
