"""  blog/context_processors.py """

from . import models

def base_context(request):
    """base_context"""
    if request:
        pass
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Topic.objects.get_topics()

    return {'authors': authors, 'topics': topics}
