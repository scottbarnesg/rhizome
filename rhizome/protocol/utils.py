from typing import Dict


class Serializable:
    def serialize(self):
        return self.__dict__

    def deserialize(self, data: Dict[str, any]):
        self.__dict__ = data
