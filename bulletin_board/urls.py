"""bulletin_board URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mmorpg.views import UserView, UserUpdate, PostList, CommentListFiltered

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/', include('allauth.urls')),
    path('user/', UserView.as_view()),
    path('user/edit/<int:pk>/', UserUpdate.as_view(), name='user_edit'),
    path('', PostList.as_view(), name='post_list'),
    path('post/', include('mmorpg.urls')),
    path('post/search/', CommentListFiltered.as_view(), name='comment_search'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
