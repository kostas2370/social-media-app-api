from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Post, PostImage
from app1.models import User
from PIL import Image
import tempfile


class PostTestCase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username = 'admin', password = 'pass@123', email = 'admin@admin.com',
                                         date_of_birth = "2007-06-06", is_public = True)
        self.user1.set_password("pass@123")
        self.user1.is_verified = True
        self.user1.save()

        self.user2 = User.objects.create(username = 'admin2', password = 'pass@123', email = 'admin2@admin.com',
                                         date_of_birth = "2007-06-06", is_public = True, is_official = True)
        self.user2.set_password("pass@123")
        self.user2.is_verified = True
        self.user2.save()

        self.user3 = User.objects.create(username = 'admin3', password = 'pass@123', email = 'admin3@admin.com',
                                         date_of_birth = "2007-06-06", is_public = False)
        self.user3.set_password("pass@123")
        self.user3.is_verified = True
        self.user3.save()

        self.user1.friends.add(self.user3)

    def test_add_post(self) -> None:
        self.client.force_authenticate(self.user1)
        image = Image.new('RGBA', size = (50, 50), color = (155, 12, 0))
        file = tempfile.NamedTemporaryFile(suffix = '.png', delete = False)
        image.save(file)
        with open(file.name, 'rb') as image:
            response1 = self.client.post(reverse("addpost"), {"upload_image": [image], "title": "renato", "text": "kekw",
                                                              "is_public": "True"}, format = 'multipart')
            response2 = self.client.post(reverse("addpost"),
                                         {"upload_image": [image], "title": "renato", "text": "kekw",
                                          "is_public": "True", "tags": ["aek", "renato"]}, format = 'multipart')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

    def test_get_feed(self) -> None:
        Post.objects.create(author = self.user1, text = "kekw", is_public = True)
        Post.objects.create(author = self.user2, text = "kekw", is_public = True)
        Post.objects.create(author = self.user3, text = "kekw", is_public = True)
        Post.objects.create(author = self.user1, text = "kekw", is_public = False)

        self.client.force_authenticate(self.user2)
        response1 = self.client.get(reverse("getfeed"))

        self.client.force_authenticate(self.user1)
        response2 = self.client.get(reverse("getfeed"))

        self.assertEqual(len(response1.data), 2)
        self.assertEqual(len(response2.data), 2)

    def test_delete_post(self) -> None:
        post1 = Post.objects.create(author = self.user1, text = "kekw", is_public = True)
        post2 = Post.objects.create(author = self.user2, text = "kekw", is_public = True)
        self.client.force_authenticate(self.user1)
        response1 = self.client.delete(reverse("deletepost", kwargs = {"post_id": post1.id}))
        response2 = self.client.delete(reverse("deletepost", kwargs = {"post_id": post2.id}))

        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post(self) -> None:
        post1 = Post.objects.create(author = self.user1, text = "kekw", is_public = True)
        self.client.force_authenticate(self.user1)
        response1 = self.client.put(reverse("updatepost", kwargs = {"post_id": post1.id}), data = {"title": "titlos",
                                                                                                   "text": "xxxx"})
        self.client.force_authenticate(self.user3)
        response2 = self.client.put(reverse("updatepost", kwargs = {"post_id": post1.id}), data = {"title": "titlos2"
                                                                                                   , "text": "xxxx"})
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

