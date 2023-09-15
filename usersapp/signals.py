import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from .tasks import send_email


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_password_url = f"{instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm'))}?token={reset_password_token.key}"
    send_email("Password Reset", reset_password_token.user.email, reset_password_url)


"""
@receiver(post_save,sender = User)
def send_status(sender, instance, created, **kwargs):
    if not created :
        channel_layer = get_channel_layer()
        user = instance.id
        user_status = instance.is_online

        data = {
            'id': user,
            'status': user_status
        }
        async_to_sync(channel_layer.group_send)(
            'user', {
                "type":'send_status',
                "value": json.dumps(data)
                     }
        )


"""
