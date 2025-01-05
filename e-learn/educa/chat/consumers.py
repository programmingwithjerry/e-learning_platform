"""
This module defines the `ChatConsumer` for handling WebSocket connections in a chat application.

The consumer handles WebSocket events such as connecting, disconnecting, and message processing.
Messages are sent to a group corresponding to a course's chat room, and they are also persisted
to the database for chat history.

Classes:
    ChatConsumer: Manages WebSocket communication for course chat rooms.
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone

from chat.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat in course rooms.

    Methods:
        connect: Establishes a WebSocket connection and joins the corresponding chat group.
        disconnect: Removes the connection from the chat group when the socket is closed.
        persist_message: Saves chat messages to the database.
        receive: Handles incoming WebSocket messages, broadcasting them to the group and persisting.
        chat_message: Sends a broadcasted message back to the WebSocket client.
    """

    async def connect(self):
        """
        Handles a new WebSocket connection.

        Retrieves the user and course ID from the WebSocket scope, assigns the user to a group
        corresponding to the chat room, and accepts the WebSocket connection.
        """
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles WebSocket disconnection.

        Removes the user from the chat group corresponding to the room.
        """
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def persist_message(self, message: str):
        """
        Persists a chat message to the database.

        Args:
            message: The message content to save.
        """
        await Message.objects.acreate(
            user=self.user, course_id=self.id, content=message
        )

    async def receive(self, text_data: str):
        """
        Handles incoming WebSocket messages.

        Parses the message data, sends it to the group for broadcast, and persists it
        in the database.

        Args:
            text_data: JSON-formatted string containing the chat message.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # Send message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.user.username,
                'datetime': now.isoformat(),
            },
        )

        # Persist the message to the database
        await self.persist_message(message)

    async def chat_message(self, event: dict):
        """
        Handles messages broadcasted by the group.

        Sends the received message back to the WebSocket client.

        Args:
            event: Dictionary containing the broadcasted message data.
        """
        await self.send(text_data=json.dumps(event))
