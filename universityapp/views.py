from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UniversitySerializer, UniversityReviewSerializer, UniversityFollowerSerializer, \
    UniversityPostSerializer
from django.http.response import JsonResponse
from rest_framework import status
from usersapp import utils
from . models import *
from django.shortcuts import get_object_or_404
from django.http import QueryDict


# Create your views here.

@api_view(["POST"])
def register_university(request):

    if not request.user.is_verified:
        return JsonResponse("Your account must be verified, to apply for university",
                            status = status.HTTP_401_UNAUTHORIZED, safe = False)

    request.data["admin"] = request.user.id
    serializer = UniversitySerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
def get_university(request, slug=None, id=None):
    if not request.user.is_verified:
        return JsonResponse("Your account must be verified, to check for universities",
                            status = status.HTTP_401_UNAUTHORIZED, safe = False)

    if id is not None:
        university = University.objects.filter(id = id)

    elif slug is not None:
        university = University.objects.filter(slug = slug)

    else:
        university = University.objects.all()[:10]

    serializer = UniversitySerializer(university, many = True)
    return Response(serializer.data)


@api_view(["POST"])
def add_university_review(request):
    university = University.objects.get(id = request.data["university"])

    if not request.user.is_verified:
        return JsonResponse("Your account must be verified, to check for universities",
                            status = status.HTTP_401_UNAUTHORIZED)

    if not utils.check_if_university_domain(request.user.email) == university.id:

        return JsonResponse("You must have the same email domain with the university",
                            status = status.HTTP_401_UNAUTHORIZED, safe = False)

    request.data["user"] = request.user.id

    serializer = UniversityReviewSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def add_follower(request, university):
    if not request.user.is_verified:
        return JsonResponse("Your account must be verified, to follow universities",
                            status = status.HTTP_401_UNAUTHORIZED)

    uni = get_object_or_404(University, id = university)
    uni_follow = UniversityFollower.objects.filter(university = uni, user = request.user)
    if len(uni_follow) == 0:
        obj = UniversityFollower.objects.create(university = uni, user = request.user)
        obj.save()
        return Response(UniversityFollowerSerializer(obj).data)
    else:
        uni_follow[0].delete()

    return JsonResponse("The follow deleted successfully",
                        status = status.HTTP_204_NO_CONTENT, safe = False)


@api_view(["POST"])
def add_post(request):

    if type(request.data) is QueryDict:
        request.data._mutable = True

    university = University.objects.get(id = request.data["university"])
    if not request.user.id == university.admin.id:
        return JsonResponse("You must be the admin to add university post",
                            status = status.HTTP_401_UNAUTHORIZED, safe = False)

    request.data["author"] = request.user.id
    images = request.FILES.getlist('upload_image')
    serializer = UniversityPostSerializer(data = request.data, context={'upload_image': images})
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return Response(data = serializer.data, status = status.HTTP_201_CREATED)

