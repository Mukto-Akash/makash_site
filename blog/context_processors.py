"""  blog/context_processors.py """

from . import models

def base_context(request):
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Topic.objects.get_topics()

    return {'authors': authors, 'topics': topics}