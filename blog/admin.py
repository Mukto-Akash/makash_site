""" blog/admin.py """
from django.contrib import admin
from . import models

# Register your models here.

class CommentInline(admin.StackedInline):
    model = models.Comment
    extra = 0
    readonly_fields = ('name', 'email', 'text')
    can_delete = False


# Register the `Post` model
class PostAdmin(admin.ModelAdmin):
    """Class for Post objects"""
    list_display = (
        'title',
        'created',
        'updated',
        #'author',
        #'status',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
        'topics',
    )
    
    inlines = [
        CommentInline,
    ]


    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    """Class for Topic objects"""
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Comment) #new
class CommentAdmin(admin.ModelAdmin):
    """Class for comment objects"""
    list_display = (
        'name',
        'email',
        'text',
        'approved',
    )
    search_fields=(
        'text',
        'name',
        'post',
    )
    list_filter=(
        'approved',
    )