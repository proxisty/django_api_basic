from django.contrib import admin
from .models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('created', 'title', 'body', 'owner')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('created', 'body', 'owner', 'post')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Category)
