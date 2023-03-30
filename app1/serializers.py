from .models import User, FriendRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, use_url=True, allow_empty_file = False)
    sex = serializers.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'password', "email", "date_of_birth", "profile_image", "sex")
        extra_kwargs = {'password': {'write_only': True}, }


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only = True)
    password = serializers.CharField(write_only = True)
    tokens = serializers.DictField(read_only = True)

    class Meta:
        model = User
        fields = ("username", "password", "tokens")

    def validate(self, attrs):
        username = attrs.get("username", '')
        password = attrs.get("password", '')

        auser = authenticate(username = username, password = password)
        if not auser:
            raise AuthenticationFailed("There is not a user with that credentials")
        if not auser.is_verified:
            raise AuthenticationFailed("You have to verify your account to be able to have access to your account")
        if not auser.is_active:
            raise AuthenticationFailed("Your account is not active contant our support to reactivate it")

        return {
            "tokens": auser.get_tokens()
        }
        return super().validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "sex", "profile_image", "is_official", "is_verified")


class PostUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('username', 'id', "is_official", "profile_image")


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user", "accepted")


