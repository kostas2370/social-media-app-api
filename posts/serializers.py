from .models import Post, PostImage, Comment, Likes, Dislikes
from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from app1.serializers import UserSerializer


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ["post", "image"]


class CommentsSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source = "author.username", read_only = True)

    class Meta:
        model = Comment
        fields = ["post", "id", "author", "release_date", "text", "author_name"]


class PostSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    title = serializers.CharField(required = False)
    author = UserSerializer()
    images = PostImageSerializer(many = True)
    upload_image = serializers.ListSerializer(
        child = serializers.ImageField(max_length = 10000000, allow_empty_file = False,
                                       use_url = False, write_only = True))
    comments = CommentsSerializer(many = True)
    likes = serializers.IntegerField(source = "likes.count")
    dislikes = serializers.IntegerField(source = "dislikes.count")

    class Meta:
        model = Post
        fields = ["id", "title", "author", "text", "release_date", "tags", "post_images", "comments", "likes",
                  "dislikes", "upload_image"]

    def create(self, validated_data):
        images = validated_data.pop("upload_image")
        post = Post.objects.create(**validated_data)

        for image in images:
            PostImage.objects.create(post = post, image = image)

        return post


