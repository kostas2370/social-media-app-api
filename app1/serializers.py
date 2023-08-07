from .models import User, FriendRequest
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers
from django.contrib.auth import authenticate
from datetime import datetime
from dateutil import relativedelta
from .utils import check_if_university_domain


class RegisterSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False, use_url=True, allow_empty_file = False)
    sex = serializers.CharField(required = False)

    class Meta:
        model = User
        fields = ('username', 'password', "email", "date_of_birth", "profile_image", "sex")
        extra_kwargs = {'password': {'write_only': True}, }

    def validate(self, attrs):
        def conds(password: str) -> bool:
            passwordCheck = [lambda s: any(x.isupper() for x in s),
                             lambda s: any(x.islower() for x in s),
                             lambda s: any(x.isdigit() for x in s),
                             lambda s: len(s) >= 8, ]

            return all(condition(password) for condition in passwordCheck)

        email = attrs.get("email")

        password = attrs.get("password")

        if relativedelta.relativedelta(datetime.now(), attrs.get("date_of_birth")).years < 18:

            raise AuthenticationFailed("You must be over 18")

        if not conds(password):
            raise AuthenticationFailed("Your password must contain at least 8 chars ,uppercase ,lowercase ,digit")

        if not check_if_university_domain(email):

            raise AuthenticationFailed("Your email must be academic email")

        return super().validate(attrs)


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



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "date_of_birth", "sex", "profile_image", "is_official", "is_verified",
                  "is_active")


class PostUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ('username', 'id', "is_official", "profile_image")


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ("id", "from_user", "accepted")


