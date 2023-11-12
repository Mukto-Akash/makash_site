"""blogs/views.py"""
# from typing import Any, Dict
from django.shortcuts import render
from django.http import HttpResponse
# from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
# from django.db.models import Count, Sum

from . import forms, models
# Create your views here.

#---------------------------------------------------------------------------
class TopicListView(ListView):
    """List view of topics to show on /topic/"""
    template_name = 'blog/topic_list.html'

    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.order_by('name') # sort alphabetically

class TopicDetailView(DetailView):
    """View to show all the posts related to a topic"""
    template_name = 'blog/topic_detail.html'
    model = models.Topic

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get the current topic
        topic = self.get_object()

        # Add in a QuerySet of all the posts
        context['posts'] = topic.blog_posts.all()
        context['num_posts'] = context['posts'].count()
        return context
# ---------------------------------------------------------------------------------

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
    # topics = models.Topic.objects.get_topics()
    topics = models.Topic.objects.all()

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

    # ------------------------------------------------
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = self.get_object()
        related_topics = current_post.topics.all()
        context['related_topics'] = related_topics
        return context

    #------------------------

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

def form_example(request):
    """Create an instance of the form"""
    form = forms.ExampleSignupForm()
    # Handle the POST
    if request.method == 'POST':
        # Pass the POST data into a new form instance for validation
        form = forms.ExampleSignupForm(request.POST)

        # If the form is valid, return a different template
        if form.is_valid():
            # form.cleaned_data is a dict with valid form data
            cleaned_data = form.cleaned_data

            return render(
                request,
                'blog/form_example_success.html',
                context={'data': cleaned_data}
            )
        # If not a POST, return a blank form
        else:
            form = forms.ExampleSignupForm()

    # Render the form and pass it into the context
    # Return if either an invalid POST or a GET
    return render(request, 'blog/form_example.html', context={'form': form})

class FormViewExample(FormView):
    """Class based FormView"""
    template_name = 'blog/form_example.html'
    form_class = forms.ExampleSignupForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """Create a "success" message"""
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you for signing up!'
        )
        # Continue with default behaviour
        return super().form_valid(form)

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)