from django.urls import path
from .views import get_university, register_university, add_university_review, add_post
urlpatterns = [
    path('university/<slug:slug>', get_university, name="university_profile"),
    path('university/id/<int:id>', get_university, name = "university_id"),
    path('university/', get_university, name = "random_universities"),
    path("university/register/", register_university, name = "university_register"),
    path("university/review/", add_university_review, name = "university_add_review"),
    path("university/post/new/", add_post, name = "university_post_new")
]

