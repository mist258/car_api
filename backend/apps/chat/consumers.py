import json
from datetime import datetime

import pytz
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from djangochannelsrestframework.decorators import action


class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        self.room_name = None
        self.user_name = None
        super().__init__(*args, **kwargs)


    async def connect(self):

        tz = pytz.timezone('Europe/Kiev')
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        if not self.scope['user']:
            return await self.close()
        self.room_name = self.scope['url_route']['kwargs']['room']
        self.user_name = await self.get_user_name()
        await self.accept()
        await self.channel_layer.group_add(self.room_name,
                                           self.channel_name)
        await self.channel_layer.group_send(self.room_name,
                                            {
                                                'type': 'sender',
                                                'message': f'{self.user_name} joined the room {self.room_name}',
                                                'timestamp': timestamp,
                                            }
                                            )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json.get('message', '')
                request_id = text_data_json.get('request_id', '')
                action = text_data_json.get('action', 'send_message')

                if action == 'send_message':
                    await self.send_message(message, request_id, action)
            except json.JSONDecodeError:
                await self.send(text_data=json.dumps({
                    'error': 'Invalid JSON format'
                }))

    @action()
    async def send_message(self, data, request_id, action):

        tz = pytz.timezone('Europe/Kiev')
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'sender',
                'message': data,
                'user': self.user_name,
                'id': request_id,
                'timestamp': timestamp,
            }
        )

    async def sender(self, data):
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def get_user_name(self):
        user = self.scope['user']
        return user.profile.first_name
