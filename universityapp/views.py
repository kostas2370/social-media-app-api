from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UniversitySerializer, UniversityReviewSerializer
from django.http.response import JsonResponse
from rest_framework import status
from usersapp import utils
from . models import *

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



