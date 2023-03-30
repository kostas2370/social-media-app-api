from rest_framework.decorators import api_view
from rest_framework.response import Response
from app1.models import IpAddress
from .models import Post
from .serializers import PostSerializer
from app1.utils import get_ip


@api_view(["GET"])
def get_post(request):
    posts = Post.objects.all()
    ipa = get_ip(request)
    ips = IpAddress.objects.filter(ip = ipa).all()

    if ips.count() == 0:

        ip = IpAddress.objects.create(ip = ipa)
        ip.save()

    else:
        ip = ips[:1]

    for post in posts:

       post.add_ip(ip.get())
    return Response(PostSerializer(posts, many = True).data)

# TODO POST VIEWS
