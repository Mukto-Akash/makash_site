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
- python manage.py shell
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
- Post: for blog posts, contains subclass Meta, methods: __str__, ForeignKey(): author, choices, SlugField, models.ManyToManyField()
- Meta: subclass of Post for sorting/ordering
- PostAdmin: for list_display, search_fields, list_filter, preopoulated_fields,
- CreditRating: for models.OneToOneField(), models.IntegerField()
- Topic: for models.CharField(), models.SlugField()
- TopicAdmin: for list_display, prepopulated_fields
## Decorators:
- @admin.register(models.Topic) # used instead ofadmin.site.register
 
# Shell Commands:
### from blog.models import Post
- Post.objects.all() # Get all objects
- posts = Post.objects.all()
- posts[0]
- Post.objects.count()
- Post.objects.filter(title='hello world!') # Case dependent
- Post.objects.filter(title__iexact='hello world!')  # iexact: insensitive-exact
- Post.objects.filter(title__icontains='admin') # lookup
- Post.objects.filter(id__gt=4) # gt, ly, gte, lte
- Post.objects.get(pk=4)
- post = Post()
- repr(post) # Creates empty post
- post.save()
### from django.contrib.auth.models import User
- user = User.objects.get(username='makash')
- post.author = user
- post.id # auto generated primary key
- post.pk
- post = Post(author=user, title='Hello world!') # must be followed by post.save()
- post = Post.objects.create(author=user, title='Another post!') # create and save
- post.title = 'A post from the Django shell' # followed by post.save to update
- post.delete()
- posts = [Post(author=user) for _ in range(3)]  # Create some instances
- Post.objects.bulk_create(posts)  # Save all
- Post.objects.filter(title='').update(title='TODO: give me a title')
- Post.objects.bulk_update(posts, ['title']) # Updates individual titles
- Post.objects.filter(title__contains='TODO').delete()
- user.blog_posts.all() # reverse accessor using related_name = 'blog_posts'
### from credit.models import CreditRating
- rating = CreditRating(user=user, score=800)
- rating.save()
- user.credit_rating
- rating.user
### from blog.models import Post, Topic
-  post = topic.blog_posts.first() # Grab first element in the list
- post.topics.all()
- post = Post.objects.create(title='M2M', author=user, slug='m2m')
- topic = Topic.objects.create(name='ORM', slug='orm')
- post.topics.add(topic)
- post.topics.remove(topic)
- post.topics.clear() # remove() and clear() methods do not delete the topics; they dissassociate topics from posts.
### from django.db.models import Q
- Post.objects.filter(Q(status='draft') | Q(title__startswith='Django'))
- Post.objects.filter(Q(status='draft') & Q(title__icontains='admin') & ~Q(topics__name='ORM'))
- Post.objects.filter(topics__name__in=['Python', 'ORM'])
- users = User.objects.annotate(Count('blog_posts'))
- users[0].blog_posts__count
- User.objects.annotate(Count('blog_posts')).values('username', 'blog_posts__count') # return all objects as dictionaries
- User.objects.annotate(total_posts=Count('blog_posts')).values('username', 'total_posts')
- users = User.objects.annotate(total_posts=Count('blog_posts'))
- users.order_by('-total_posts').values('username', 'total_posts')
### from django.db.models import Avg, Count
- User.objects.annotate(total_posts=Count('blog_posts')).aggregate(avg_posts=Avg('total_posts'))

