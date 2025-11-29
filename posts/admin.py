from django.contrib import admin
from .models import Post, Status, Comment


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'author', 'status', 'created_on']
    list_filter = ['created_on', 'author', 'status']
    search_fields = ['title', 'subtitle', 'body']
    date_hierarchy = 'created_on'
    prepopulated_fields = {'subtitle': ('title',)}
    raw_id_fields = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_on', 'body_preview']
    list_filter = ['created_on', 'author']
    search_fields = ['author__username', 'body', 'post__title']
    date_hierarchy = 'created_on'
    raw_id_fields = ['author', 'post']
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Comment Preview'
