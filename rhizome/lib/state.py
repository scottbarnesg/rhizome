from typing import Dict

from rhizome.protocol.utils import Serializable


class RhizomeState(Serializable):
    def __init__(self, method: str, state: Dict[str, any]):
        self.method = method
        self.state = state



