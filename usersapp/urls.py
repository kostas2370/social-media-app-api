from django.urls import path, include
from .views import send_friend_request, accept_friend_request, get_friend_request, delete_friend, get_friend\
                   , get_friend_of_other, get_user, change_password


urlpatterns = [
    path('sendrequest/<int:touserid>', send_friend_request, name="send_friend_request"),
    path('acceptrequest/<int:requestid>', accept_friend_request, name="accept_friend_request"),
    path('getrequest/', get_friend_request, name="get_friend_request"),
    path('deletefriend/<int:friendid>', delete_friend, name="delete_friend"),
    path('getfriend/', get_friend, name = "get_friend"),
    path('getfriend/<int:otherid>', get_friend_of_other, name = "get_friend_of_other"),
    path('user/<int:user_id>', get_user, name = "get_user"),
    path('user/', get_user, name = "get_my_info"),
    path('user/password/update', change_password, name = "password_change"),
    path('user/password_reset/', include('django_rest_passwordreset.urls', namespace = 'password_reset')),

]

