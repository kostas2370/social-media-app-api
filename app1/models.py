from django.db import models
from django.contrib.auth.models import AbstractUser
import app1.tasks as tasks


class User(AbstractUser):
    sex_choices =(('M', 'MALE'), ('F', 'FEMALE'), ('O', 'OTHER'))
    email = models.EmailField(unique = True)
    date_of_birth = models.DateField()
    profile_image = models.ImageField(default = "default.jpg",upload_to = "profile_pics")
    sex = models.CharField(default = 'O', choices =sex_choices, max_length = 1)
    friends = models.ManyToManyField("User", blank = True)
    is_public = models.BooleanField(default = True)

    REQUIRED_FIELDS = ["email", "date_of_birth"]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super().save()
        tasks.resize_image.delay(self.profile_image.path, 184, 184)

    def check_if_friend(self, other) -> bool:
        if other in self.friends.all():
            return True

        return False


class Message(models.Model):

    id = models.AutoField(primary_key= True)
    sender = models.ForeignKey(User, on_delete = models.CASCADE, blank = False, related_name= 'SenderToRec')
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, blank = False, related_name ='recToSencer')
    message = models.CharField(max_length = 500, blank = False)
    image = models.ImageField(upload_to = "message_pics", blank = True, null = True)
    created = models.DateTimeField(auto_now_add = True)
    isRead = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.sender} to {self.recipient} {self.id}"

    def isread(self):
        self.isRead = True
        self.save()


class FriendRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(User, related_name = 'from_user', on_delete = models.CASCADE)
    to_user = models.ForeignKey(User, related_name = 'to_user', on_delete = models.CASCADE)
    accepted = models.BooleanField(default = False)

    def friend_accept(self):
        self.accepted = True
        self.save()

    def __str__(self):
        return f"{self.id} : {self.from_user.username} to {self.to_user.username}"


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, blank = True)
    text = models.TextField(blank = True)
    release_date = models.DateField(auto_now = True)
    is_public = models.BooleanField(default = False)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)

    def add_like(self):
        self.likes += 1
        self.save()

    def add_dislike(self):
        self.dislikes += 1
        self.save()

    def __str__(self):
        return id


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "images")
    image = models.ImageField(upload_to = "post_images", null = False)

    def save(self, *args, **kwargs):
        super().save()
        tasks.change_jpg.delay(self.image)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    release_date = models.DateField(auto_now = True)
    text = models.CharField(max_length = 300, blank = False, null = False)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)

    def __str__(self):
        return f"{id} : {self.author.username}"

    def add_like(self):
        self.likes += 1
        self.save()

    def add_dislike(self):
        self.dislikes += 1
        self.save()
