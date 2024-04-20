from django.contrib import admin
from .models import PostImage, Post, Likes, Dislikes, Comment, PostView

# Register your models here.

admin.site.register(PostImage)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Dislikes)
admin.site.register(Comment)
admin.site.register(PostView)


