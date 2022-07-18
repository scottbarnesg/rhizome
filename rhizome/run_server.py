import socket

from rhizome.protocol.server import RhizomeServer


if __name__ == '__main__':
    sender_id = socket.gethostname()
    rhizome_server = RhizomeServer(sender_id)
    rhizome_server.start_in_background()
    while True:
        if rhizome_server.has_message():
            message = rhizome_server.get_message()
            print(f"Got message: {message.encode()}")


