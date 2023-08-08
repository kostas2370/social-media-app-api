"""SocialMediaApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from usersapp.registerview import UserRegisterView, VerifyEmail
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django.urls import path, include
from usersapp.registerview import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/token/', LoginView.as_view(), name="login"),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', UserRegisterView.as_view(), name="register"),
    path('api/email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('api/', include("usersapp.urls")),
    path('api/', include("posts.urls"))
]
