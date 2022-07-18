import socket

from rhizome.protocol.client import RhizomeClient
from rhizome.protocol.messages import BroadcastMessage


if __name__ == '__main__':
    # Create client
    sender_id = socket.gethostname()
    rhizome_client = RhizomeClient(sender_id)
    # Create message
    message = BroadcastMessage(sender_id, socket.gethostname(), 54321)
    # Send message
    host = "localhost"
    port = 54321
    rhizome_client.send_message(message, host, port)
    # Get responses
