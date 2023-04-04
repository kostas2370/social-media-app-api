from .models import Post, PostImage, Comment, Likes, Dislikes
from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from app1.serializers import PostUserSerializer


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = ["post", "id", "image"]
        extra_kwargs = {'post': {'write_only': True}, }


class CommentsSerializer(serializers.ModelSerializer):
    author = PostUserSerializer()

    class Meta:
        model = Comment
        fields = ["post", "id", "author", "release_date", "text"]
        extra_kwargs = {'post': {'write_only': True}, }


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    tags = TagListSerializerField()
    title = serializers.CharField(required = False)
    post_images = PostImageSerializer(many = True, read_only = True)
    upload_image = serializers.ListSerializer(
        child = serializers.ImageField(max_length = 10000000, allow_empty_file = False,
                                       use_url = False), required = False, write_only = True)
    comments = CommentsSerializer(many = True, read_only = True)
    likes = serializers.IntegerField(source = "likes.count", read_only = True)
    dislikes = serializers.IntegerField(source = "dislikes.count", read_only = True)
    views = serializers.IntegerField(source = "views.count", read_only = True)
    is_public = serializers.BooleanField()

    class Meta:
        model = Post
        fields = ["id", "title", "author", "text", "upload_date", "tags", "post_images", "comments", "likes",
                  "dislikes", "upload_image", "views", "is_public"]

    def create(self, validated_data):
        print(validated_data)
        images = []
        if validated_data.get("upload_image"):
            images = validated_data.pop("upload_image")

        post = Post.objects.create(**validated_data)

        for image in images:
            PostImage.objects.create(post = post, image = image)

        return post

    def to_representation(self, instance):
        self.fields["author"] = PostUserSerializer()
        return super(PostSerializer, self).to_representation(instance)

    def update(self, instance, validated_data):
        instance.tags = validated_data.get('tags', instance.tags)
        instance.title = validated_data.get('title', instance.title)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        images = validated_data.get("upload_image")
        if images:
            instance.post_images.clear()
            for image in images:
                PostImage.objects.create(post = instance, image = image)
        instance.save()
        return instance

