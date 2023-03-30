from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .tasks import send_email
from rest_framework import status
from .models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


class UserRegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)

        if serializer.is_valid(raise_exception = True):
            serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data["email"])
        user.set_password(request.data["password"])
        user.save()
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        link = reverse('email-verify')
        absurl = f'{current_site}{link}?token={str(token)}'

        send_email.delay("Register verification", user.email, f"Thank you, here is the verification link : {absurl}")

        return Response(UserSerializer(user).data, status = status.HTTP_201_CREATED)


class VerifyEmail(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        token = request.GET.get('token')
        try:
            load = jwt.decode(token, settings.SECRET_KEY, algorithms = 'HS256')
            user = User.objects.get(id = load['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            else:
                return Response({"error": "User is already verified"}, status = status.HTTP_400_BAD_REQUEST)

            return Response({"email": "Successfuly Activated"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as error:
            return Response({"error": "Token Expired"}, status = status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as error:
            return Response({"error": "Invalid Token"}, status = status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)

        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)