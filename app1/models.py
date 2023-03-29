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
    is_official = models.BooleanField(default = False)

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


