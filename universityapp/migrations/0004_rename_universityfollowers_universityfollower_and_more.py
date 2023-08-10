# Generated by Django 4.0.3 on 2023-08-10 16:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('universityapp', '0003_rename_universities_university_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UniversityFollowers',
            new_name='UniversityFollower',
        ),
        migrations.RenameModel(
            old_name='UniversityPosts',
            new_name='UniversityPost',
        ),
        migrations.RenameModel(
            old_name='UniversityPostImages',
            new_name='UniversityPostImage',
        ),
        migrations.RenameModel(
            old_name='UniversityReviews',
            new_name='UniversityReview',
        ),
    ]
