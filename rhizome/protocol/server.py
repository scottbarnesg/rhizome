import queue
import socketserver
import threading
from typing import Tuple

from rhizome.protocol.messages import Message, BroadcastResponse, get_message_type
from rhizome.protocol.peers import KnownPeers, Peer


class RhizomeConnectionHandler(socketserver.StreamRequestHandler):
    BUFFER_SIZE = 1024

    def handle(self):
        # Read data from socket
        message_data = self.request.recv(self.BUFFER_SIZE).strip()
        # Convert into message class
        message_type = get_message_type(message_data)
        message = message_type()
        message.decode(message_data)
        # Push message to server queue
        self.server.add_message(message)
        # Add client to known peers
        peer = Peer(message.sender_id, self.client_address[0], self.client_address[1])
        KnownPeers().add_peer(peer)
        # Reply with broadcast response
        response = BroadcastResponse(self.server.sender_id)
        self.request.sendall(response.encode())


class RhizomeServer(socketserver.TCPServer):
    def __init__(self, sender_id: str,
                 server_address: Tuple[str, int] = ("localhost", 54321),
                 request_handler: socketserver.StreamRequestHandler = RhizomeConnectionHandler):
        self.sender_id = sender_id
        self.server_address = server_address
        self.message_queue = queue.Queue()
        self.server_thread = None
        socketserver.TCPServer.__init__(self, server_address, request_handler)

    def start(self):
        self.serve_forever()

    def start_in_background(self):
        self.server_thread = threading.Thread(target=self.serve_forever, daemon=True)
        self.server_thread.start()
        print(f"Started RhizomeServer on {self.server_address[0]}:{self.server_address[1]}.")

    def add_message(self, message: Message):
        self.message_queue.put(message)

    def has_message(self) -> bool:
        return not self.message_queue.empty()

    def get_message(self) -> Message:
        return self.message_queue.get()
