"""blogs/views.py"""
from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.

def blog(request):
    """blog"""
    if request:
        pass
    return HttpResponse('Hello World!')
