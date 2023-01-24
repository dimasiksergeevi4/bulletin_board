from django.urls import path
from .views import (
   PostList, PostSearch, PostDetail, PostCreate, PostUpdate,
   PostDelete, AppointmentView, CategoryListView, subscribe,
)
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.decorators import login_required

from sign.views import upgrade_me

urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='new'),
   path('search/', PostSearch.as_view(), name='search'),
   path('news/create/', login_required(PostCreate.as_view()), name='news_create'),
   path('article/create/', login_required(PostCreate.as_view()), name='post_create'),
   path('news/<int:pk>/edit/', login_required(PostUpdate.as_view()), name='news_edit'),
   path('article/<int:pk>/edit/', login_required(PostUpdate.as_view()), name='post_edit'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
   path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
   path('sign/upgrade/', upgrade_me, name='upgrade_me'),

   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

   path('mail/', AppointmentView.as_view(template_name='appointment_created.html'), name='appointment'),
]
