from typing import Tuple, Set


class Peer:
    def __init__(self, sender_id: str, hostname: str, port: int):
        self.sender_id = sender_id
        self.hostname = hostname
        self.port = port

    def get_addr(self) -> Tuple[str, int]:
        return self.hostname, self.port

    def __eq__(self, other: "Peer") -> bool:
        return (self.hostname, self.port) == other.get_addr()

    def __hash__(self):
        return hash((self.hostname, self.port))


class KnownPeers:
    """
    Borg pattern to collect known peers
    """

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.peers = set()

    def add_peer(self, peer: Peer):
        self.peers.add(peer)

    def get_peers(self) -> Set[Peer]:
        return self.peers



