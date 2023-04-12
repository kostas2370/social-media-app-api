from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post, PostImage
from .serializers import PostSerializer, CommentsSerializer
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
    friend_posts = Post.objects.filter(
                                       upload_date__lte = date.today(),
                                       upload_date__gte = datet,
                                       author__friends = request.user,
                                       ).order_by("?")[:60]

    official_posts = Post.objects.filter(
                                         upload_date__lte = date.today(),
                                         upload_date__gte = date.today() - timedelta(days = 7),
                                         author__is_official = True
                                         ).exclude(author__friends = request.user
                                                   ).order_by("?")[:30]

    random_posts = Post.objects.filter(
                                       upload_date__lte = date.today(),
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
    images = request.FILES.getlist('upload_image')
    serializer = PostSerializer(data = request.data, context={'upload_image': images})
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(data = serializer.data, status = status.HTTP_201_CREATED)


@api_view(["DELETE"])
def delete_post(request, post_id):
    post = get_object_or_404(Post, id = post_id)

    if post.author != request.user:
        return Response({"Message": "UNAUTHORIZED"}, status = status.HTTP_401_UNAUTHORIZED)

    post.delete()
    return Response({"Message": "Post got deleted successfully"}, status = status.HTTP_204_NO_CONTENT)


@api_view(["PUT"])
def update_post(request, post_id):
    post = get_object_or_404(Post, id= post_id)
    if post.author != request.user:
        return Response({"Message": "UNAUTHORIZED"}, status = status.HTTP_401_UNAUTHORIZED)

    images = request.FILES.getlist('upload_image')
    serializer = PostSerializer(instance = post, data = request.data, partial = True, context = {'upload_image': images}
                                )
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data)


@api_view(["DELETE"])
def delete_post_image(request, post_id, image_id):
    post = get_object_or_404(Post, id = post_id)
    if post.author != request.user:
        return Response({"Message": "UNAUTHORIZED"}, status = status.HTTP_401_UNAUTHORIZED)

    image = get_object_or_404(PostImage, post = post, id = image_id)
    image.delete()
    return Response({"Message": "Image deleted"}, status = status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def add_post_like(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.add_like(request.user)
    return Response({"Message": "Like added successfully"}, status = status.HTTP_201_CREATED)


@api_view(["POST"])
def add_post_dislike(request, post_id):
    post = get_object_or_404(Post, id = post_id)
    post.add_dislike(request.user)

    return Response({"Message": "Dislike added successfully"}, status = status.HTTP_201_CREATED)


@api_view(["POST"])
def add_post_comment(request, post_id):
    request.data["author"] = request.user.id
    request.data["post"] = post_id
    serializer = CommentsSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    serializer.save()

    return Response({"Message": "Comment created successfully"}, status = status.HTTP_201_CREATED)

