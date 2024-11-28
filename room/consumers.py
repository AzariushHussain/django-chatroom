import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    live_users = {}

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        self.user = self.scope['user']
        self.username = self.user.username if self.user.is_authenticated else "Anonymous"

        if self.room_group_name not in ChatConsumer.live_users:
            ChatConsumer.live_users[self.room_group_name] = set()

        ChatConsumer.live_users[self.room_group_name].add(self.username)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_joined',
                'user': self.username
            }
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'You are connected to the chat room.',
            'live_users': list(ChatConsumer.live_users[self.room_group_name])
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_left',
                'user': self.username
            }
        )

        if self.room_group_name in ChatConsumer.live_users:
            ChatConsumer.live_users[self.room_group_name].discard(self.username)
            if not ChatConsumer.live_users[self.room_group_name]:
                del ChatConsumer.live_users[self.room_group_name]

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        user_id = self.scope['user'].id
        user = self.scope['user'].username

        await self.save_message(user_id, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'user': user
        }))

    async def user_joined(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user': user
        }))

    async def user_left(self, event):
        user = event['user']
        await self.send(text_data=json.dumps({
            'type': 'user_left',
            'user': user
        }))

    @database_sync_to_async
    def save_message(self, user_id, message_content):
        from room.models import Message, Room
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        room = Room.objects.get(id=self.room_id)
        message = Message.objects.create(
            user=user,
            message=message_content,
            room=room
        )
        return message
