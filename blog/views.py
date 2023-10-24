"""blogs/views.py"""
from django.shortcuts import render
from django.http import HttpResponse
from . import models
# Create your views here.

def blog(request):
    """blog"""
    if request:
        pass
    return HttpResponse('Hello World!')

def home(request):
    """The blog homepage"""
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:10]
    # Add as context variable "latest_posts"
    # context = {'latest_posts': latest_posts}
    # authors = models.Post.objects.get_authors()
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Topic.objects.get_topics()

    context = {
        'authors': authors,
        'topics': topics,
        'latest_posts': latest_posts
    }

    return render(request, 'blog/home.html', context)
