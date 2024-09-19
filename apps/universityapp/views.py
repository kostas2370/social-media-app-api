from rest_framework.response import Response
from .serializers import UniversitySerializer, UniversityReviewSerializer, UniversityFollowerSerializer, \
    UniversityPostSerializer
from django.http.response import JsonResponse
from rest_framework import status
from . models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.decorators import action
from .permissions import UniversityPermissions, ReviewPermission


class UniversityViewSet(ModelViewSet):
    serializer_class = [UniversitySerializer]
    permission_classes = [IsAuthenticated, UniversityPermissions, ReviewPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    pagination_class = [PageNumberPagination]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return University.objects.all()

        return University.objects.filter(Q(admin = self.request.user) | Q(is_active = True))

    def get_serializer_class(self):
        if self.action == "review":
            return UniversityReviewSerializer

        if self.action == "post":
            return UniversityPostSerializer

        return UniversitySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        upload_image = self.request.FILES.getlist('upload_image')
        if upload_image:
            context["upload_image"] = upload_image

        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)

    @action(detail = True, methods = ["POST"])
    def review(self, request, pk):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)

    @action(detail = True, methods = ["POST"])
    def follow(self, request, pk):
        uni = self.get_object()
        uni_follow = UniversityFollower.objects.filter(university = uni, user = request.user)
        if len(uni_follow) == 0:
            obj = UniversityFollower.objects.create(university = uni, user = request.user)
            obj.save()
            return Response(UniversityFollowerSerializer(obj).data)
        else:
            uni_follow[0].delete()

        return JsonResponse("The follow deleted successfully", status = status.HTTP_204_NO_CONTENT, safe = False)

    @action(detail = True, methods = ["POST"])
    def post(self, request, pk):
        data = request.data
        data["university"] = pk
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_201_CREATED)



