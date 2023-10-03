# mukto_site
Projects in Python django

# Description
Django project mukto_site created for OLRN1508 by Mukto Akash.

# Commands Used:
- django-admin startproject mukto_site .
- python manage.py runserver
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py startapp blog
- python manage.py makemigrations
- pytest and pylint

# Files created/altered:
- view.py
- test_views.py
- url.py
- pytest.ini
- settings.py
- blog/models.py
- blog/admin.py

# Packages
All packages used are in requirements.txt created using pip freeze

# Apps Created
- blog
## Classes:
- Post: for blog posts, contains subclass Meta, methods: __str__, ForeignKey(): author, choices, SlugField,
- Meta: subclass of Post for sorting/ordering
- PostAdmin: for list_display, search_fields, list_filter, preopoulated_fields,
 
