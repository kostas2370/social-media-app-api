from .models import University, UniversityFollower, UniversityReview, UniversityPost, UniversityPostImage
from apps.usersapp.serializers import PostUserSerializer
from rest_framework import serializers


class UniversityPostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UniversityPostImage
        fields = ["post", "id", "image"]
        extra_kwargs = {'post': {'write_only': True}, }


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ["id", "name", "admin", "email_domain", "university_profile", "is_active"]
        extra_kwargs = {'id': {'read_only': True}, "is_active": {"read_only": True}}


class UniversityFollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityFollower
        fields = "__all__"

    def to_representation(self, instance):
        self.fields["user"] = PostUserSerializer()
        return super(UniversityFollowerSerializer, self).to_representation(instance)


class UniversityReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UniversityReview
        fields = "__all__"
        extra_kwargs = {'reply': {'read_only': True}, }

    def to_representation(self, instance):
        self.fields["user"] = PostUserSerializer()
        return super(UniversityReviewSerializer, self).to_representation(instance)


class UniversityPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(required = False)
    university_post_images = UniversityPostImageSerializer(many = True, read_only = True)

    class Meta:
        model = UniversityPost
        fields = ["id", "university", "author", "title", "text", "upload_date", "university_post_images"]

    def create(self, validated_data):
        images = self.context["upload_image"]
        post = UniversityPost.objects.create(**validated_data)
        if images:
            for image in images:
                UniversityPostImage.objects.create(post = post, image = image)

        return post

    def to_representation(self, instance):
        self.fields["author"] = PostUserSerializer()
        return super(UniversityPostSerializer, self).to_representation(instance)

