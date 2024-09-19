from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.usersapp.utils import get_ip
from .models import Post, PostImage
from .serializers import PostSerializer, CommentsSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .permissions import PostPermissions


class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated, PostPermissions]

    def get_serializer_class(self):
        return PostSerializer
    def get_serializer_context(self):
        context = super().get_serializer_context()
        upload_image = self.request.FILES.getlist('upload_image')
        if upload_image:
            context["upload_image"] = upload_image

        return context

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = PostSerializer(obj)
        return Response(serializer.data)

    def list(self, request):
        publisher = request.GET.get("publisher", None)
        if publisher:
            author = get_object_or_404(get_user_model(), id = publisher)
            posts = Post.objects.filter(Q(author = author),
                                        Q(author__is_public = True) | Q(author__friends = request.user))
        else:
            posts = Post.objects.filter(author = request.user)

        serializer = self.get_serializer(posts, many = True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        post = self.get_object()
        post.delete()
        return Response({"Message": "Post got deleted successfully"}, status = status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        post = self.get_object()
        images = request.FILES.getlist('upload_image')
        serializer = PostSerializer(instance = post, data = request.data, partial = True,
                                    context = {'upload_image': images})

        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    @action(detail = True, methods = ["DELETE"])
    def delete_post_image(self, request, pk):
        post = self.get_object()
        image = get_object_or_404(PostImage, post = post, id = request.GET.get("image_id"))
        image.delete()
        return Response({"Message": "Image deleted"}, status = status.HTTP_204_NO_CONTENT)

    @action(detail = True, methods = ["PATCH"])
    def like(self, request, pk):
        post = self.get_object()
        post.add_like(request.user)
        return Response({"Message": "Like added successfully"}, status = status.HTTP_201_CREATED)

    @action(detail = True, methods = ["PATCH"])
    def dislike(self, request, pk):
        post = self.get_object()
        post.add_dislike(request.user)
        return Response({"Message": "Dislike added successfully"}, status = status.HTTP_201_CREATED)

    @action(detail = True, methods = ["POST"])
    def comment(self, request, pk):
        post = self.get_object()
        data = {"post": post.id, "text": request.data.get("text")}
        serializer = CommentsSerializer(data =data, context = self.get_serializer_context())
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({"Message": "Comment created successfully"}, status = status.HTTP_201_CREATED)

    @action(detail = False, methods = ["GET"])
    def get_feed(self, request):
        datet = date.today()-timedelta(days = 30)
        ipa = get_ip(request)

        posts = Post.objects.filter(Q(  # Friend posts conditions
            Q(upload_date__lte = date.today()) & Q(upload_date__gte = datet) & Q(author__friends = request.user) & Q(
                views__times_count__lt = 5)) | Q(  # Official posts conditions
            Q(upload_date__lte = date.today()) & Q(upload_date__gte = date.today()-timedelta(days = 7)) & Q(
                author__is_official = True) & Q(views__times_count__lt = 5) & ~Q(author__friends = request.user)) | Q(
            Q(upload_date__lte = date.today()) & Q(upload_date__gte = datet) & Q(is_public = True) & Q(
                author__is_public = True) & Q(author__is_official = False) & Q(views__times_count__lt = 5) & ~Q(
                author__friends = request.user)  # Exclude user's friends
        )).order_by("?")[:60]

        for post in posts:
            post.add_view(ipa, request.user)

        return Response(PostSerializer(posts, many = True).data)
