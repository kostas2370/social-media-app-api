from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


@api_view(["GET"])
def get_post(request):
    posts = Post.objects.all()
    return Response(PostSerializer(posts, many = True).data)

#TODO POST VIEWS