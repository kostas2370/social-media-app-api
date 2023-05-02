from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app1.models import User
import json


class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'current_user'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, message):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_status(self, event):
        data = json.loads(event.get("value"))
        user_id = data["id"]
        online_status = data["status"]

        await self.send(text_data = json.dumps({
            'user_id': user_id,
            'online_status': online_status
        }))

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        user_id = data["user_id"]
        connection_type = data["type"]

        await self.change_status(user_id,connection_type)

    @database_sync_to_async
    def change_status(self, user_id, type):
        user = User.objects.get(id = user_id)
        if type == "open":
            user.is_online = True
        else:
            user.is_online = False

        user.save()