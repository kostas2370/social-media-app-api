from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.response import Response
from . import tasks
from rest_framework import status
from .models import FriendRequest, User
from .serializers import FriendRequestSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from .serializers import PostUserSerializer, ChangePasswordSerializer
from django.contrib.auth import update_session_auth_hash


@api_view(["GET"])
def get_friend_request(request) -> Response:
    myrequests = FriendRequest.objects.filter(to_user = request.user)
    serializer = FriendRequestSerializer(myrequests, many = True)
    return Response(serializer.data)


@api_view(["POST"])
def send_friend_request(request, touserid) -> JsonResponse:

    from_user = request.user
    to_user = User.objects.get(id = touserid)
    if to_user.check_if_friend(from_user):
        return JsonResponse("You are already friends", status = status.HTTP_400_BAD_REQUEST)

    swapped = FriendRequest.objects.filter(to_user = from_user, from_user = to_user)

    if swapped.count() == 1:
        swapped.first().friend_accept()
        from_user.friends.add(to_user)
        to_user.friends.add(from_user)
        return JsonResponse({"Message": f"{to_user.username} and you are friends now"}, status = status.HTTP_201_CREATED
                            )

    friend_req, created = FriendRequest.objects.get_or_create(from_user=from_user, to_user = to_user)
    friend_req.save()

    if not created:
        return JsonResponse({"Message": "Friend Request already sent !"}, status = status.HTTP_400_BAD_REQUEST)

    tasks.send_email.delay("You got a friend request", to_user.email, f" You have received a friend request from "
                                                                      f"{from_user.username}")
    return JsonResponse({"Message": "Your friend request got sent successfully"}, status = status.HTTP_200_OK)


@api_view(["PUT"])
def accept_friend_request(request, requestid) -> JsonResponse:
    friend_request = FriendRequest.objects.get(id= requestid)
    if not friend_request.to_user == request.user:
        return JsonResponse({"Message": "You do not have permission"}, status = status.HTTP_406_NOT_ACCEPTABLE)

    if request.user.check_if_friend(friend_request.from_user):
        return JsonResponse({"Message": "You are already friends"}, status = status.HTTP_404_NOT_FOUND)

    request.user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(request.user)

    friend_request.friend_accept()
    return JsonResponse({"Message": "Friend accepted"}, status = status.HTTP_200_OK)


@api_view(["GET"])
def get_friend(request):
    friends = [friend for friend in request.user.friends.all()]
    return Response(PostUserSerializer(friends, many = True).data)


@api_view(["GET"])
def get_friend_of_other(request,otherid):
    other = User.objects.get(id= otherid)
    if not other.is_public and not other.check_if_friend(request.user):
        return JsonResponse({"Message": "This profile is private"}, status = status.HTTP_404_NOT_FOUND)

    friends = []
    for friend in other.friends.all():
        if friend.check_if_friend(request.user) or friend.is_public:
            friends.append(friend)

    return Response(PostUserSerializer(friends, many = True).data)


@api_view(["DELETE"])
def delete_friend(request, friendid) -> JsonResponse:
    user = request.user
    friend = User.objects.get(id=friendid)
    if not user.check_if_friend(friend):
        return JsonResponse({"Message": "Not in the friend list"}, status = status.HTTP_404_NOT_FOUND)

    user.friends.remove(friend)
    friend.friends.remove(user)

    from_friend = FriendRequest.objects.filter(from_user = user, to_user = friend)
    to_friend = FriendRequest.objects.filter(from_user = friend, to_user = user)
    if from_friend.exists():
        from_friend[:1].get().delete()
    else:
        to_friend[:1].get().delete()

    return JsonResponse({"Message": "Friend deleted successfully"}, status = status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def get_user(request, user_id=None):
    if user_id is None:
        return Response(UserSerializer(request.user).data)

    user = get_object_or_404(User, id = user_id)

    if not user.is_public and not user.check_if_friend(request.user):
        return JsonResponse({"Message": "You dont have access at that profile"}, status = status.HTTP_401_UNAUTHORIZED)

    else:
        return Response(UserSerializer(user).data)


@api_view(["POST"])
def change_password(request):

    serializer = ChangePasswordSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)
    user = request.user

    if user.check_password(serializer.data.get("old_password")):
        user.set_password(serializer.data.set("new_password"))
        user.save()
        update_session_auth_hash(request, user)
        return Response({'message': 'Password changed successfully.'}, status = status.HTTP_200_OK)

    return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)

