from .message import MessageBody
from ..base.consul_and_hz_service import ConsulAndHazelcastService

class HazelCastLoggingService(ConsulAndHazelcastService):
    service_name: str = "logging-service"

    def __init__(self, port: int) -> None:
        super().__init__(self.service_name, port)
        self.logging_map = self.hz_client.get_map("logging-map")

    def add_message(self, msg: MessageBody):
        self.logging_map.set(msg.uuid, msg.text).result()

    def get_messages(self):
        return self.logging_map.values().result()
