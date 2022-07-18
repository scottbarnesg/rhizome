import queue
import threading
import socket


class RhizomeNetwork:
    def __init__(self):
        self.discovered_peers = queue.Queue()

    def listen_for_broadcasts(self):
        # TODO: Listen for broadcasts in a background thread. Add discovered peers to self.discovered_peers
        pass

    def broadcast(self):
        # TODO: Broadcast our uuid
        pass
