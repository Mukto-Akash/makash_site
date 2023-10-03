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
    )

admin.site.register(models.Post, PostAdmin)