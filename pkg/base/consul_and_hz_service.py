import sys
import json
import consul
import logging
import hazelcast
import logging.config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class ConsulAndHazelcastService:
    def __init__(self, service_name: str, port: int) -> None:
        self.service_definition = {
            "name": service_name,
            "service_id": f"{service_name}_{port}",
            "address": "127.0.0.1",
            "port": port,
            "check": {
                "http": f"http://127.0.0.1:{port}/health",
                "interval": "10s"
            }
        }
        self.consul_client = consul.Consul()
        self.hz_client = hazelcast.HazelcastClient(
            cluster_members=json.loads(self.consul_client.kv.get("hazelcast-cluster-members")[1]['Value']),
            cluster_name=self.consul_client.kv.get("hazelcast-cluster-name")[1]['Value'].decode()
        )

    def register_service(self):
        self.consul_client.agent.service.register(**self.service_definition)
        logger.info("Service registered in Consul.")

    def deregister_and_shutdown(self):
        self.hz_client.shutdown()
        self.consul_client.agent.service.deregister(self.service_definition["service_id"])
        logger.info("Service removed from Consul.")