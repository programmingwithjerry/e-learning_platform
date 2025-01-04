import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    """
    ChatConsumer is a WebSocket consumer that handles communication in a chat room.
    It allows clients to connect to a specific course chat room, send messages,
    and receive messages from other participants in real-time using Django Channels.
    """

    async def connect(self):
        """
        Handles the WebSocket connection.

        This method is called when the WebSocket connection is established.
        It retrieves the course ID from the URL, joins the corresponding room group,
        and accepts the connection.

        The room group name is dynamically created based on the course ID.
        """
        self.user = self.scope['user']
        # Retrieve course ID from the URL route parameters
        self.id = self.scope['url_route']['kwargs']['course_id']
        # Construct the room group name using the course ID
        self.room_group_name = f'chat_{self.id}'

        # Join the room group to receive messages sent to this group
        await self.channel_layer.group_add(
            self.room_group_name,  # The room group name
            self.channel_name      # The unique channel name for this connection
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection.

        This method is called when the WebSocket connection is closed. It removes
        the WebSocket connection from the room group, so it no longer receives
        messages.

        Args:
            close_code (int): The close code provided when the WebSocket is closed.
        """
        # Leave the room group to stop receiving messages
        await self.channel_layer.group_discard(
            self.room_group_name,  # The room group name
            self.channel_name      # The unique channel name for this connection
        )

    async def receive(self, text_data):
        """
        Handles receiving a message from the WebSocket.

        This method is called when a message is received through the WebSocket.
        It parses the message from JSON format and sends it to the room group
        to be broadcast to other participants.

        Arg:
            text_data (str): The message data received from the WebSocket, in JSON format.
        """
        # Parse the received message from JSON
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,  # The room group name
            {
                'type': 'chat_message',  # The type of message being sent
                'message': message,      # The message content
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )

    async def chat_message(self, event):
        """
        Handles receiving a message from the room group.

        This method is called when a message is received from the room group.
        It sends the message to the WebSocket to be displayed to the client.

        Arg:
            event (dict): The event data received from the room group.
                          Contains the message to be sent to the WebSocket.
        """
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(event))
