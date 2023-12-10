"""blogs/apps.py"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """BlogConfig class"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
