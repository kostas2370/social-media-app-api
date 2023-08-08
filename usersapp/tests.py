from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User, FriendRequest


# Create your tests here.


class UserTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username = 'admin', password = 'pass@123', email = 'admin@admin.com',
                                        date_of_birth = "2007-06-06")
        self.user.set_password("pass@123")
        self.user.is_verified = True
        self.user.save()

    def test_register(self) -> None:
        data1 = {"username": "pagotos", "password": "Mastoras123", "email": "test@gmail.com",
                 "date_of_birth": "2002-06-07"}
        data2 = {"username": "pagotos1", "password": "mastoras123", "email": "test@gmail.com",
                 "date_of_birth": "06-06-2001"}
        data3 = {"username": "adminAss", "password": "Pass@123a", "email": "admin@ieseg.fr", "date_of_birth": "2014-06-07"}

        response1 = self.client.post(reverse("register"), data = data1, format = "json")
        response2 = self.client.post(reverse("register"), data = data2, format = "json")
        response3 = self.client.post(reverse("register"), data = data3, format = "json")

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_403_FORBIDDEN)

    def test_login(self):
        response1 = self.client.post(reverse("login"), data = {"username": "admin", "password": "pass@123"})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.user.is_verified = False
        self.user.save()
        response2 = self.client.post(reverse("login"), data = {"username": "admin", "password": "pass@123"})
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)


class FriendTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username = 'admin', password = 'pass@123', email = 'admin@admin.com',
                                         date_of_birth = "2007-06-06")
        self.user1.set_password("pass@123")

        self.user2 = User.objects.create(username = 'mastor2', password = 'pass@123', email = 'admin2@admin.com',
                                         date_of_birth = "2007-06-06")
        self.user2.set_password("pass@123")

        self.user3 = User.objects.create(username = 'mastor3', password = 'pass@123', email = 'admin3@admin.com',
                                         date_of_birth = "2007-06-06")
        self.user3.set_password("pass@123")

    def test_send_friend_request(self) -> None:
        self.client.force_authenticate(self.user1)
        response1 = self.client.post(reverse("send_friend_request", kwargs = {'touserid': self.user2.id}))
        response2 = self.client.post(reverse("send_friend_request", kwargs = {'touserid': self.user2.id}))
        self.client.force_authenticate(self.user2)
        response3 = self.client.post(reverse("send_friend_request", kwargs = {'touserid': self.user1.id}))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_accept_friend_request(self) -> None:
        FriendRequest.objects.create(from_user = self.user1, to_user = self.user3)
        self.client.force_authenticate(self.user3)

        current_friend_req = FriendRequest.objects.get(from_user = self.user1, to_user = self.user3)
        response1 = self.client.put(reverse("accept_friend_request", kwargs = {'requestid': current_friend_req.id}))
        response2 = self.client.put(reverse("accept_friend_request", kwargs = {'requestid': current_friend_req.id}))

        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_friend(self) -> None:
        FriendRequest.objects.create(from_user = self.user1, to_user = self.user3)

        self.client.force_authenticate(self.user1)
        self.user1.friends.add(self.user3)
        self.user3.friends.add(self.user1)

        response1 = self.client.delete(reverse("delete_friend", kwargs = {"friendid": self.user3.id}))
        response2 = self.client.delete(reverse("delete_friend", kwargs = {"friendid": self.user3.id}))

        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_friend(self) -> None:
        self.user1.friends.add(self.user3)
        self.client.force_authenticate(self.user1)

        response1 = self.client.get(reverse("get_friend"))
        self.client.force_authenticate(self.user2)
        response2 = len(self.client.get(reverse("get_friend")).content)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2, 2)  # 2 means 0

    def test_get_friend_of_friends(self) -> None:
        self.user1.friends.add(self.user2)
        self.user2.friends.add(self.user1)
        self.user1.is_public = False
        self.user1.save()

        self.client.force_authenticate(self.user3)
        response1 = self.client.get(reverse("get_friend_of_other", kwargs = {"otherid": self.user1.id}),)
        self.assertEqual(response1.status_code, status.HTTP_404_NOT_FOUND)

        self.client.force_authenticate(self.user2)
        response2 = self.client.get(reverse("get_friend_of_other", kwargs = {"otherid": self.user1.id}),)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.user3)
        self.user1.is_public = True
        self.user1.save()
        response3 = self.client.get(reverse("get_friend_of_other", kwargs = {"otherid": self.user1.id}),)
        self.assertEqual(response3.status_code, status.HTTP_200_OK)

    def test_get_user(self) -> None:
        self.client.force_authenticate(self.user1)
        response1 = self.client.get(reverse("get_user", kwargs = {"user_id": self.user2.id}))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.user3.is_public = False
        self.user3.save()
        response2 = self.client.get(reverse("get_user", kwargs = {"user_id": self.user3.id}))
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
        response3 = self.client.get(reverse("get_my_info"))
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
