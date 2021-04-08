import json
from channels.generic.websocket import AsyncWebsocketConsumer

class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.unique_id = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'user_%s' % self.unique_id

        print("Connecting a user to user_%s"%self.unique_id)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def status_message(self, event):
        connect = event['connect']
        message = event['message'] if 'message' in event else ''

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status',
            'connect': connect,
            'message': message
        }))

    async def initial_game_status(self, event):
        status = event['status']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'game_status',
            'status': status,
        }))