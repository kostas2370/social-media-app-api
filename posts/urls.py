from django.urls import path
from .views import get_feed, add_post
urlpatterns = [
    path("feed", get_feed, name = "testurl"),
    path("new", add_post, name = "addpost"),


]

# TODO ADD URLS
