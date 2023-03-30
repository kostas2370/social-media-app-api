from django.db import models
from app1 import tasks
from app1.models import User
from taggit.managers import TaggableManager
from app1.models import IpAddress


class Post(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100, blank = True, null = True)
    text = models.TextField(blank = True)
    release_date = models.DateField(auto_now = True)
    is_public = models.BooleanField(default = False)
    tags = TaggableManager()
    views = models.ManyToManyField(IpAddress, blank = True)

    def add_ip(self,ip):
        if ip not in self.views.all():
            self.views.add(ip.id)

    def add_like(self, user: User):
        if Dislikes.objects.filter(post = self, user = user).all().count() >= 1:
            Dislikes.objects.get(post = self, user = user).delete()

        likes = Likes.objects.filter(post = self, user = user).all()
        if likes.count() == 0:
            Likes.objects.create(post = self, user = user)
        else:
            likes[:1].delete()

    def add_dislike(self, user):

        if Likes.objects.filter(post = self, user = user).all().count() == 1:
            Likes.objects.get(post = self, user = user).delete()

        dislikes = Dislikes.objects.filter(post = self, user = user).all()
        if dislikes.count() == 0:
            Dislikes.objects.create(post = self, user = user)
        else:
            dislikes[:1].delete()

    def get_likes(self):
        return self.likes.objects.all().count()

    def get_dislikes(self):
        return self.dislikes.objects.all().count()

    def __str__(self):
        return str(self.id)


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "post_images")
    image = models.ImageField(upload_to = "post_images", blank = True, null = True)

    def save(self, *args, **kwargs):
        super().save()
        tasks.change_jpg.delay(self.image.path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    id = models.AutoField(primary_key = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    release_date = models.DateField(auto_now = True)
    text = models.CharField(max_length = 300, blank = False, null = False)

    def __str__(self):
        return f"{self.id} : {self.author.username}"


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "likes")
    user = models.ForeignKey(User, on_delete = models.CASCADE)


class Dislikes(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "dislikes")
    user = models.ForeignKey(User, on_delete = models.CASCADE)

#  TODO CHECK IF THERE IS A NEED FOR MORE FIELDS


