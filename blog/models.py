""""blog/models.py"""

from django.db import models
from django.conf import settings  # Imports Django's loaded settings
from django.utils import timezone

# Create your models here.

class Topic(models.Model):
    """Topic class"""
    name = models.CharField(
        max_length = 50,
        unique = True # No dublicates!
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        """Meta"""
        ordering = ['name']

class PostManager(models.Manager):
    """limited to records that have not been deleted"""
    def get_queryset(self):
        """Exclude deleted"""
        queryset = super().get_queryset()  # Get the initial queryset
        return queryset.exclude(deleted=True)  # Exclude deleted records

class PostQuerySet(models.QuerySet):
    """blog posts can either be published or in draft mode"""
    def published(self):
        """returns published"""
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        """returns drafts"""
        return self.filter(status=self.model.DRAFT)

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length=255)
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        help_text='The date & time this article was published',
        unique_for_date='published',  # Slug is unique for publication date
    )
    deleted = models.BooleanField()
    objects = PostManager()
    objects = PostQuerySet.as_manager()

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone


    class Meta:
        """Meta"""
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']


    def __str__(self):
        return str(self.title)
