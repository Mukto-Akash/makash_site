"""  blog/context_processors.py """

from . import models
from django.db.models import Count

def base_context(request):
    """base_context"""
    if request:
        pass
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    # topics = models.Topic.objects.get_topics()
    top_topics = models.Topic.objects.annotate(total_posts=Count('blog_posts')).order_by('-total_posts').distinct()[:5]
    topics = models.Topic.objects.all()

    return {'authors': authors, 'topics': topics, 'top_topics': top_topics}
