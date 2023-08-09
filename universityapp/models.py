from django.db import models
from usersapp.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from usersapp import tasks


class Universities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique = True, max_length = 60)
    admin = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    email_domain = models.CharField(max_length = 50)
    university_profile = models.ImageField(default = "default.jpg", upload_to = "universities_pic")
    is_active = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.name} {self.id}"


class UniversityFollowers(models.Model):
    university = models.ForeignKey(Universities, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"


class UniversityReviews(models.Model):
    id = models.AutoField(primary_key= True)
    university = models.ForeignKey(Universities, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 1, validators = [MaxValueValidator(5), MinValueValidator(1)], blank = True)
    review = models.TextField(max_length = 500)
    reply = models.CharField(max_length = 500)

    def __str__(self):
        return f"{self.university.name} {self.user.username}"

    class Meta:
        unique_together = ('university', 'user')


class UniversityPosts(models.Model):
    id = models.AutoField(primary_key=True)
    university = models.ForeignKey(Universities, on_delete = models.CASCADE, related_name = "universities_posts")
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 110, blank = True, null = True)
    text = models.TextField(blank = True)
    upload_date = models.DateField(auto_now = True)

    def __str__(self):
        return f"{self.university} post {self.id}"


class UniversityPostImages(models.Model):

    post = models.ForeignKey(Universities, on_delete = models.CASCADE, related_name = "post_images")
    image = models.ImageField(upload_to = "university_post_images", blank = True, null = True)

    def save(self, *args, **kwargs):
        super().save()
        tasks.change_jpg.delay(self.image.path)