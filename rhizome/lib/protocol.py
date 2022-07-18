# TODO: This should let developers set state in their code

import socket
import uuid

from rhizome.lib.state import RhizomeState
from rhizome.protocol.client import RhizomeClient
from rhizome.protocol.messages import StateMessage, BroadcastMessage
from rhizome.protocol.peers import KnownPeers, Peer
from rhizome.protocol.server import RhizomeServer


class RhizomeProtocol:
    def __init__(self, listen_hostname: str = "localhost", listen_port: int = 54321):
        self.id = f"{socket.gethostname()}_{uuid.uuid4().hex}"
        print(f"RhizomeProtocol uuid: {self.id}")
        self.listen_hostname = listen_hostname
        self.listen_port = listen_port
        self.rhizome_server = RhizomeServer(self.id, (self.listen_hostname, self.listen_port))
        self.rhizome_client = RhizomeClient(self.id)

    def start(self, node_hostname: str, node_port: int):
        # Start server in background
        self.rhizome_server.start_in_background()
        # Send broadcast message in background & find peers
        message = BroadcastMessage(self.id, self.listen_hostname, self.listen_port)
        try:
            self.rhizome_client.send_message(message, node_hostname, node_port)  # TODO: Need to broadcast instead of specifying IP here
            broadcast_response = self.rhizome_client.wait_for_message(BroadcastMessage)
            new_peer = Peer(broadcast_response.sender_id, broadcast_response.hostname, broadcast_response.port)
            KnownPeers().add_peer(new_peer)
        except ConnectionError:
            return

    def share_state(self, state: RhizomeState):
        # Emit StateMessage to known peers
        for peer in KnownPeers().get_peers():
            message = StateMessage(self.id, state)
            self.rhizome_client.send_message(message, peer.get_addr()[0], peer.get_addr()[1])
