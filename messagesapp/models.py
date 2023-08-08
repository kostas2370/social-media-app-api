from django.db import models
from usersapp.models import User


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

    def isRead(self):
        self.isRead = True
        self.save()

