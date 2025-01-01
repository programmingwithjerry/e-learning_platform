import json  # Import the JSON module to handle JSON serialization and deserialization
from channels.generic.websocket import WebsocketConsumer  # Import base WebSocket consumer class

# Define a WebSocket consumer for handling chat functionality
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        """
        Handle a new WebSocket connection.
        """
        # Accept the incoming WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        """
        Handle WebSocket disconnection.

        Args:
            close_code: The close code provided when the connection is closed.
        """
        pass  # No specific action needed on disconnect in this example

    def receive(self, text_data):
        """
        Handle incoming data from the WebSocket.
        Args:
            text_data: The raw JSON-encoded string sent by the client.
        """
        # Parse the incoming JSON string to a Python dictionary
        text_data_json = json.loads(text_data)
        # Extract the 'message' field from the JSON data
        message = text_data_json['message']
        # Send the same message back to the WebSocket as a JSON-encoded string
        self.send(text_data=json.dumps({'message': message}))
