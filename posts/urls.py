from django.urls import path
from .views import get_feed, add_post, get_post, update_post, delete_post, delete_image
urlpatterns = [
    path("feed", get_feed, name = "testurl"),
    path("post/new", add_post, name = "addpost"),
    path("post/", get_post, name = "getpost"),
    path("post/<int:post_id>/delete", delete_post, name = "deletepost"),
    path("post/<int:post_id>/update", update_post, name = "updatepost"),
    path("post/<int:post_id>/<int:image_id>", delete_image, name = "delete_image")

]

# TODO ADD URLS
