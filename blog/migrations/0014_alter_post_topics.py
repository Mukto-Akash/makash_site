# Generated by Django 4.2.5 on 2023-10-10 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_alter_post_topics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='topics',
            field=models.ManyToManyField(blank=True, related_name='blog_posts', to='blog.topic'),
        ),
    ]
