import hazelcast
from .message import MessageBody

class HazelCastLoggingService:
    def __init__(self) -> None:
        self.client = hazelcast.HazelcastClient()
        self.logging_map = self.client.get_map("logging-map")

    def add_message(self, msg: MessageBody):
        self.logging_map.set(msg.uuid, msg.text).result()
    
    def get_messages(self):
        return self.logging_map.values().result()
