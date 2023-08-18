from django.db import models
from usersapp import tasks
from usersapp.models import User
from taggit.managers import TaggableManager


class Post(models.Model):

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "posts")
    title = models.CharField(max_length = 110, blank = True, null = True)
    text = models.TextField(blank = True)
    upload_date = models.DateField(auto_now = True)
    is_public = models.BooleanField(default = False)
    tags = TaggableManager()

    def add_view(self, ip, user):

        gt_ip = PostView.objects.filter(post = self, user = user)

        if gt_ip .count() == 0:
            PostView.objects.create(ip = ip, post = self, user = user)
        else:
            bruh = gt_ip.first()
            bruh.times_count += 1
            bruh.save()

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
        return f"{str(self.id)} {self.title}"


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

    class Meta:
        unique_together = ('post', 'user')


class Dislikes(models.Model):

    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "dislikes")
    user = models.ForeignKey(User, on_delete = models.CASCADE)

#  TODO CHECK IF THERE IS A NEED FOR MORE FIELDS
    class Meta:
        unique_together = ('post', 'user')


class PostView(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "views")
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "viewer")
    ip = models.CharField(max_length = 15)
    times_count = models.IntegerField(default = 1)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('post', 'user')
