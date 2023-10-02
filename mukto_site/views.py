""" Views for django project mukto_site/views.py
"""

from django.http import HttpResponse


def index(request):
    """Returns html of what is to be printed"""
    response = ""
    if request:
        response = 'CG-OLRN1508-Assignment-1 <br> Mukto Akash'
    return HttpResponse(response)
    