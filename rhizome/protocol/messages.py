import json

from rhizome.lib.state import RhizomeState
from rhizome.protocol.utils import Serializable


class Message(Serializable):
    def __init__(self, sender_id: str = None, message_type: str = None):
        super(Message, self).__init__()
        self.message_length: int
        self.sender_id: str = sender_id
        self.message_type = message_type

    def encode(self) -> bytes:
        self._calculate_message_length()
        return json.dumps(self.serialize()).encode()

    def decode(self, raw_message: bytes):
        self.deserialize(json.loads(raw_message.decode()))

    def _calculate_message_length(self):
        # Run twice, once to set initial value and another to get actual value
        initial_message_length = len(json.dumps(self.serialize()).encode())
        self.message_length = initial_message_length
        corrected_message_length = len(json.dumps(self.serialize()).encode())
        self.message_length = corrected_message_length
        # If the number of digits in corrected_message_length changed, update the message length
        message_digit_change = len(str(initial_message_length)) - len(str(corrected_message_length))
        if message_digit_change:
            self.message_length += message_digit_change


class BroadcastMessage(Message):
    message_type = "broadcast-message"

    def __init__(self, sender_id: str = None, sender_hostname: str = None, sender_port: int = None):
        super(BroadcastMessage, self).__init__(sender_id, self.message_type)
        self.hostname = sender_hostname
        self.port = sender_port


class BroadcastResponse(Message):
    message_type = "broadcast-response"

    def __init__(self, sender_id: str = None, sender_hostname: str = None, sender_port: int = None):
        super(BroadcastResponse, self).__init__(sender_id, self.message_type)
        self.hostname = sender_hostname
        self.port = sender_port


class StateMessage(Message):
    message_type = "state-message"

    def __init__(self, sender_id: str = None, state: RhizomeState = None):
        super(StateMessage, self).__init__(sender_id, self.message_type)
        if state:
            self.state = state.serialize()
        else:
            self.state = None


def get_message_type(message_data: bytes):
    message_str = message_data.decode()
    if BroadcastMessage.message_type in message_str:
        return BroadcastMessage
    elif BroadcastResponse.message_type in message_str:
        return BroadcastResponse
    elif StateMessage.message_type in message_str:
        return StateMessage
    raise ValueError(f"No Message class found for message: {message_str}")


