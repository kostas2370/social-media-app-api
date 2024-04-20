from celery import shared_task
from channels.layers import get_channel_layer
from datetime import date
from .tasks import send_email
from .models import User
channel_layer = get_channel_layer()


@shared_task
def check_birthday():
    users = User.objects.all()
    for user in users:
        if user.date_of_birth.strftime("%d/%m") == date.today().strftime("%d/%m"):
            message = f"Hello {user.username}, We would like to tell you Happy Birthday from Netmindz"
            send_email.delay("Happy Birthday !", user.email, message)