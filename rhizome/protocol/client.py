import socket

from rhizome.protocol.messages import Message


class RhizomeClient:
    BUFFER_SIZE = 1024

    def __init__(self, sender_id: str):
        self.sender_id = sender_id
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __del__(self):
        self._sock.close()

    def send_message(self, message: Message, target_address: str, target_port: int):
        self._sock.connect((target_address, target_port))
        self._sock.sendto(message.encode(), (target_address, target_port))

    def wait_for_message(self, message_type, timeout: int = 1):
        self._sock.settimeout(timeout)
        message_data = self._sock.recv(self.BUFFER_SIZE).strip()
        print(f"Client got message: {message_data}")
        message = message_type()
        message.decode(message_data)
        return message
