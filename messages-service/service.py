import sys
import logging
import hazelcast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class HzMessageProcessingService:
    def __init__(self) -> None:
        self.hz_client = hazelcast.HazelcastClient()
        self.hz_mq = self.hz_client.get_queue("message-queue")
        self.messages_mem = []

    def get_messages(self):
        return self.messages_mem

    def consume_messages(self):
        while True:
            new_msg = self.hz_mq.take().result()
            logger.info(f"messages-service got {new_msg}")
            self.messages_mem.append(new_msg)
            if new_msg == "":
                self.hz_mq.offer("").result()
                break
        self.hz_client.shutdown()
