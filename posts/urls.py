from django.urls import path
from .views import get_feed, add_post, get_post, update_post, delete_post, delete_post_image, add_post_like, \
    add_post_dislike, add_post_comment

urlpatterns = [
    path("feed", get_feed, name = "getfeed"),
    path("post/new", add_post, name = "addpost"),
    path("post/", get_post, name = "getpost"),
    path("post/<int:post_id>/delete", delete_post, name = "deletepost"),
    path("post/<int:post_id>/update", update_post, name = "updatepost"),
    path("post/<int:post_id>/<int:image_id>", delete_post_image, name = "deletepostimage"),
    path("post/<int:post_id>/like", add_post_like, name = "postlike"),
    path("post/<int:post_id>/dislike", add_post_dislike, name = "postdislike"),
    path("post/<int:post_id>/comment", add_post_comment, name = "postcomment"),

]

# TODO ADD URLS
