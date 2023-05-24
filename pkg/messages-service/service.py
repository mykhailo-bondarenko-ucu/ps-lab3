import sys
import logging
import hazelcast
from ..base.consul_and_hz_service import ConsulAndHazelcastService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class HzMessageProcessingService(ConsulAndHazelcastService):
    service_name: str = "messages-service"

    def __init__(self, port: int) -> None:
        super().__init__(self.service_name, port)
        self.hz_mq = self.hz_client.get_queue("message-queue")
        self.messages_mem = []

    def get_messages(self):
        return self.messages_mem

    def consume_messages(self):
        # remove poison on startup
        while (r := self.hz_mq.take().result()) == "": pass
        # re-insert non-poinsonous result
        self.hz_mq.offer(r).result()
        # start consuming loop
        while True:
            new_msg = self.hz_mq.take().result()
            logger.info(f"messages-service got {new_msg}")
            self.messages_mem.append(new_msg)
            if new_msg == "":
                # reincert poison so that all the message consumers are shut down
                self.hz_mq.offer("").result()
                break
        self.hz_client.shutdown()

    def stop_consuming(self):
        # poison the message queue to stop all the messaging consumers
        self.hz_mq.offer("").result()
