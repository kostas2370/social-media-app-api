from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('chat', self.channel_name)
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard('chat', self.channel_name)
