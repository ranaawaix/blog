from django.contrib import admin
from blog.models import Category, Post, Comment, Vote, ContactUs


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['users', 'name', 'description', 'slug']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'description', 'category', 'publish_date', 'publish', 'draft',
                    'created_on', 'updated_on', 'image', 'slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'comment', 'created_on', 'updated_on', 'slug']


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'vote', 'created_on', 'updated_on']


@admin.register(ContactUs)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'file']