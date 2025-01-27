from django.contrib import admin
from .models import Community, Post, Comment

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'community', 'created_by', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'community')
    ordering = ('-created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'created_by', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at', 'post')
    ordering = ('-created_at',)