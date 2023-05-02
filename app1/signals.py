import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
@receiver(post_save,sender = User)
def send_status(sender,instance,created,**kwargs):
    if not created :
        channel_layer = get_channel_layer()
        user = instance.user.id
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




