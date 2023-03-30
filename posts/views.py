from rest_framework.decorators import api_view
from rest_framework.response import Response
from app1.models import IpAddress
from .models import Post
from .serializers import PostSerializer
from app1.utils import get_ip
from datetime import timedelta, date
from itertools import chain


@api_view(["GET"])
def get_feed(request):
    datet = date.today() - timedelta(days = 3)
    ipa = get_ip(request)
    # TODO have to improve the filtering
    friend_posts = Post.objects.filter(upload_date__lte = date.today(),
                                       upload_date__gte = datet,
                                       is_public = True,
                                       author__friends = request. user,
                                       ).exclude(views__ip = ipa
                                                 ).order_by("?")[:60]

    official_posts = Post.objects.filter(upload_date__lte = date.today(),
                                         upload_date__gte = date.today() - timedelta(days = 7),
                                         author__is_official = True
                                         ).exclude(views__ip = ipa
                                                   ).exclude(author__friends = request.user
                                                             ).order_by("?")[:30]

    random_posts = Post.objects.filter(upload_date__lte = date.today(),
                                       upload_date__gte = datet,
                                       is_public = True,
                                       author__is_public = True,
                                       author__is_official = False,
                                       ).exclude(author__friends = request.user
                                                 ).exclude(views__ip = ipa
                                                           ).order_by("?")[:20]

    posts = list(chain(friend_posts, official_posts, random_posts))
    ips = IpAddress.objects.filter(ip = ipa).all()

    if not ips.count():

        ip = IpAddress.objects.create(ip = ipa)
        ip.save()

    else:
        ip = ips[:1]

    for post in posts:
        post.add_view(ip.get())

    return Response(PostSerializer(posts, many = True).data)

# TODO POST VIEWS
