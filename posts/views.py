from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, PostView
from .serializers import PostSerializer,PostUserSerializer
from app1.utils import get_ip
from datetime import timedelta, date
from itertools import chain
from app1.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(["GET"])
def get_feed(request):
    datet = date.today() - timedelta(days = 3)
    ipa = get_ip(request)
    # TODO have to improve the filtering
    friend_posts = Post.objects.filter(upload_date__lte = date.today(),
                                       upload_date__gte = datet,
                                       author__friends = request.user,
                                       ).order_by("?")[:60]

    official_posts = Post.objects.filter(upload_date__lte = date.today(),
                                         upload_date__gte = date.today() - timedelta(days = 7),
                                         author__is_official = True
                                         ).order_by("?")[:30]

    random_posts = Post.objects.filter(upload_date__lte = date.today(),
                                       upload_date__gte = datet,
                                       is_public = True,
                                       author__is_public = True,
                                       author__is_official = False,
                                       ).exclude(author__friends = request.user
                                                 ).order_by("?")[:20]

    posts = list(chain(friend_posts, official_posts, random_posts))

    for post in posts:
        post.add_view(ipa, request.user)

    return Response(PostSerializer(posts, many = True).data)




@api_view(["GET"])
def get_post(request):
    publisher = request.query_params.get("publisher", None)
    post_id = request.query_params.get("post_id", None)
    if publisher:
        author = get_object_or_404(User, id= publisher)
        posts = Post.objects.filter(Q(author = author),
                                    Q(author__is_public = True) | Q(author__friends = request.user)
                                    )
    elif post_id:
        posts = Post.objects.filter(id = post_id)
        if posts.count() == 0:
            return Response({"Message": "Cant find post with that id"}, status = status.HTTP_404_NOT_FOUND)

        if request.user not in posts.first().author.friends.all() and not posts.first().author.is_public:
            return Response({"Message": "You dont have access to this post"}, status = status.HTTP_401_UNAUTHORIZED)

    serializer = PostSerializer(posts, many = True)
    return Response(serializer.data)


@api_view(["POST"])
def add_post(request):
    request.data["author"] = request.user.id
    serializer = PostSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    serializer.save()

    return Response(data = serializer.data, status = status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    if post.author == request.user:
        post.delete()
        return Response({"Message": "Post got deleted succesfully"}, status = status.HTTP_204_NO_CONTENT)

    return Response({"Message": "UNAUTHORIZED"}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(["PATCH"])
def update_post(request, post_id):

    post = get_object_or_404(Post, id= post_id)
    serializer = PostSerializer(instance = post, data = request.data, partial = True)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data)

# TODO I HAVE to fix the image problem with posts
