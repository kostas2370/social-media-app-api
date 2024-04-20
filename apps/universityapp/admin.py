from django.contrib import admin
from .models import University, UniversityReview, UniversityFollower, UniversityPost, UniversityPostImage

# Register your models here.
admin.site.register(University)
admin.site.register(UniversityReview)
admin.site.register(UniversityFollower)
admin.site.register(UniversityPost)
admin.site.register(UniversityPostImage)
