"""blogs/views.py"""
from django.shortcuts import render
from django.http import HttpResponse
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

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

class PostListView(ListView):
    """PostListView"""
    model = models.Post
    context_object_name = 'posts'
    queryset = models.Post.objects.published().order_by('-published')  # Customized queryset

class PostDetailView(DetailView):
    """PostDetailView"""
    model = models.Post

    def get_queryset(self):
        queryset = super().get_queryset().published()

        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return queryset

        # Otherwise, filter on the published date
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )

# class ContextMixin:
#     """
#     Provides common context variables for blog views
#     """
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['authors'] = models.Post.objects.published().get_authors().order_by('first_name')
#         context['topics'] = models.Topic.objects.get_topics()

#         return context

# class AboutView(View):
    # def get(self, request):
    #     return render(request, 'blog/about.html')

# class AboutView(ContextMixin,TemplateView):
class AboutView(TemplateView):
    """AboutView"""
    template_name = 'blog/about.html'
#
#     def get_context_data(self, **kwargs):
#         # Get the context from the parent class
#         context = super().get_context_data(**kwargs)

#         # Define the "authors" context variable
#         context['authors'] = models.Post.objects.published().get_authors().order_by('first_name')
#         context['topics'] = models.Topic.objects.get_topics()
#
#         return context


# class HomeView(ContextMixin, TemplateView):
class HomeView(TemplateView):
    """HomeView"""
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)

        latest_posts = models.Post.objects.published() \
            .order_by('-published')[:3]

        # authors = models.Post.objects.published() \
        #     .get_authors() \
        #     .order_by('first_name')
        # topics = models.Topic.objects.get_topics()


        # Update the context with our context variables
        context.update({
            # 'authors': authors,
            'latest_posts': latest_posts,
            # 'topics': topics,
        })

        return context

def terms_and_conditions(request):
    """terms_and_conditions"""
    return render(request, 'blog/terms_and_conditions.html')
