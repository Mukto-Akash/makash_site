"""
URL configuration for OLRN_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blog import views as vw
# from . import views # Import the views module

urlpatterns = [
    #path('', views.index), # Add our index view to the URL patterns
    path('admin/', admin.site.urls),
    path('blog', vw.blog),
    # path('', vw.home, name='home'), # Set root to home view
    path('', vw.HomeView.as_view(), name='home'),
    path('about/', vw.AboutView.as_view(), name='about'),
    path('terms/', vw.terms_and_conditions, name='terms-and-conditions'),
    path('posts/', vw.PostListView.as_view(), name='post-list'),
    path(
        'posts/<int:year>/<int:month>/<int:day>/<slug:slug>/',
        vw.PostDetailView.as_view(),
        name='post-detail',
    ),
    path(
        'posts/<int:pk>/',
        vw.PostDetailView.as_view(),
        name='post-detail'
    ),
    # New for Assignment 4
    path('topics/', vw.TopicListView.as_view(), name='topic-list'),
    path('topics/<slug:slug>/', vw.TopicDetailView.as_view(), name='topic-detail'),
    #---------------------
]
