from django.db import models
from usersapp.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from usersapp import tasks
from django.urls import reverse
from django.template.defaultfilters import slugify


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(unique = True, max_length = 60)
    admin = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    email_domain = models.CharField(max_length = 50)
    university_profile = models.ImageField(default = "default.jpg", upload_to = "universities_pic")
    is_active = models.BooleanField(default = False)
    slug = models.SlugField(null = True)

    def __str__(self):
        return f"{self.name} {self.id}"

    def get_absolute_url(self):
        return reverse("university_profile", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class UniversityFollower(models.Model):
    university = models.ForeignKey(University, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.university.name}"


class UniversityReview(models.Model):
    id = models.AutoField(primary_key= True)
    university = models.ForeignKey(University, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default = 1, validators = [MaxValueValidator(5), MinValueValidator(1)], blank = True)
    review = models.TextField(max_length = 500)
    reply = models.CharField(max_length = 500)
    upload_date = models.DateField(auto_now = True)
    edit_date = models.DateField(auto_now = True)

    def __str__(self):
        return f"{self.university.name} {self.user.username}"

    class Meta:
        unique_together = ('university', 'user')


class UniversityPost(models.Model):
    id = models.AutoField(primary_key=True)
    university = models.ForeignKey(University, on_delete = models.CASCADE, related_name = "universities_posts")
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 110, blank = True, null = True)
    text = models.TextField(blank = True)
    upload_date = models.DateField(auto_now = True)

    def __str__(self):
        return f"{self.university} post {self.id}"


class UniversityPostImage(models.Model):

    post = models.ForeignKey(UniversityPost, on_delete = models.CASCADE, related_name = "university_post_images")
    image = models.ImageField(upload_to = "university_post_images", blank = True, null = True)

    def save(self, *args, **kwargs):
        super().save()
        tasks.change_jpg.delay(self.image.path)