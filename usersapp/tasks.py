from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from channels.layers import get_channel_layer
from PIL import Image

channel_layer = get_channel_layer()


@shared_task
def send_email(name, email, text):
    send_mail(subject = name, message = text, from_email = settings.EMAIL_HOST_USER, recipient_list = [email])

@shared_task
def resize_image(image: str, x: int, y: int):
    img = Image.open(image)
    if img.height > x or img.width > y:
        outputsize = (x, y)
        img.thumbnail(outputsize)
        img.save(image)


@shared_task
def change_jpg(image):
    img = Image.open(image)
    if img.format != "JPEG":
        rgb_im = img.convert("RGB")
        rgb_im.save(image)





