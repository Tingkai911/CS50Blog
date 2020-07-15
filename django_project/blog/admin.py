from django.contrib import admin
from .models import Post, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted')
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment', 'user', 'post', 'date_posted')
admin.site.register(Comment, CommentAdmin)
