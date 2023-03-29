from .models import User, FriendRequest
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, use_url=True, allow_empty_file = False)
    sex = serializers.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'password', "email", "date_of_birth", "profile_image", "sex")
        extra_kwargs = {'password': {'write_only': True}, }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "sex", "profile_image", "is_official")


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user", "accepted")

