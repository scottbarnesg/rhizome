from rhizome.protocol.utils import Serializable


class RhizomeState(Serializable):
    def __init__(self, method, state):
        self.method = method
        self.state = state



