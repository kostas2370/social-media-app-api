from django.urls import path
from .views import get_feed
urlpatterns = [
    path("getpost", get_feed, name = "testurl")

]

# TODO ADD URLS
