""""blog/models.py"""

from django.db import models
from django.conf import settings
from django.db.models.query import QuerySet  # Imports Django's loaded settings
from django.utils import timezone
from django.contrib.auth import get_user_model
# from django.db.models import Count
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

# class TopicQuerySet(models.QuerySet):
#     """Query for topics"""
#     def get_topics(self):
#         """get_topics"""
#         topics = Topic.objects.annotate(total_posts=Count('blog_posts'))
#         topics = topics.order_by('-total_posts').distinct()
#         return topics

class Topic(models.Model):
    """Topic class"""
    name = models.CharField(
        max_length = 50,
        unique = True # No dublicates!
    )
    slug = models.SlugField(unique=True)
    # objects = TopicQuerySet.as_manager()

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Absolute URL"""
        return reverse('topic-detail', kwargs={'slug': self.slug})

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
    # content = models.TextField(null=True, blank=True)
    content = RichTextUploadingField()
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
    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post',
    )
    deleted = models.BooleanField()
    objects = PostManager()
    objects = PostQuerySet.as_manager()

    def publish(self):
        """Publishes this post"""
        self.status = self.PUBLISHED
        self.published = timezone.now()  # The current datetime with timezone

    def get_absolute_url(self):
        """Absolute URL"""
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}

        return reverse('post-detail', kwargs=kwargs)

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

class Contact(models.Model):
    """Model for Contact Form"""
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta"""
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'

# Assignment 5 -----------------------------------------
class PhotoContestSubmissions(models.Model):
    """PhotoContestSubmissions"""
    first_name=models.CharField(
        max_length=255,
        null = False,
    )
    last_name=models.CharField(
        max_length=255,
        null = False,
    )
    email=models.EmailField(
        max_length=254,
        null=False,
    )
    photo=models.ImageField(
        blank=True,
        null=True,
    )
    submitted = models.DateTimeField(
        null=True,
        blank=True,
        auto_now=True,
    )

    class Meta:
        """Meta"""
        ordering = ['-submitted']
# --------------------------------------------------------
