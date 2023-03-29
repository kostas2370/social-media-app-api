from django.urls import path
from .views import get_post
urlpatterns = [
    path("getpost", get_post, name = "testurl")

]