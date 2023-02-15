from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'date_of_creation', 'category', 'title', 'content']
    list_filter = ['author', 'category']
    search_fields = ['author__username', 'title', 'content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'user', 'date_of_creation', 'text_wrap', 'approved']
    list_filter = ['user', 'approved']
    search_fields = ['text', 'date_of_creation', 'user__username']

    def text_wrap(self, obj):
        return obj.text[:50]

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
