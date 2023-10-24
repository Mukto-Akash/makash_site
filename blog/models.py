""""blog/models.py"""

from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet  # Imports Django's loaded settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Count

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

    def get_authors(self):
        """get_authors"""
        user = get_user_model()
        return user.objects.filter(blog_posts__in=self).distinct()
    
    def get_topics(self):
        """get_topics"""
        topics = Topic.objects.annotate(total_posts=Count('blog_posts')).order_by('-total_posts').distinct()
        return topics

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
    title = models.CharField(max_length=255, null = False,)
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )  # Sets on create
    updated = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )  # Updates on each save
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        null=False,
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
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts',
        blank=True
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


class CommentManager(models.Manager):
    """Comment Manager"""
    def get_queryset(self) -> QuerySet:
        """Only shows approved comments"""
        queryset = super().get_queryset()
        return queryset.exclude(approved = False) # Exclude unapproved comments

class Comment(models.Model): #new
    """Comments under the blogs app"""
    post = models.ForeignKey(
        Post,
        on_delete = models.CASCADE,
        related_name='comments',
        null=False,
    )
    name=models.CharField(
        max_length=255,
        null = False,
    )
    email=models.EmailField(
        max_length=254,
        null=False,
    )
    text=models.TextField(
        max_length=500,
    )
    approved=models.BooleanField(
        default=False,
    )
    created=models.DateTimeField(
        auto_now_add=True,
    )
    updated=models.DateTimeField(
        auto_now=True,
    )
    objects = CommentManager()

    def __str__(self):
        return str(self.text)[:50]

    class Meta:
        """Meta for ordering"""
        ordering = ['-created']
