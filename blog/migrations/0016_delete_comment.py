# Generated by Django 4.2.5 on 2023-10-10 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_comment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
