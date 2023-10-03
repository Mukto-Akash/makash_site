# blog/admin.py
from django.contrib import admin
from . import models

# Register your models here.

# Register the `Post` model
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
        'author',
        'status',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    list_filter = (
        'status',
    )
    
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(models.Post, PostAdmin)