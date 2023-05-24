import sys
import httpx
import random
import logging
import logging.config
from .message import Message
from urllib.parse import urljoin
from fastapi import HTTPException
from ..base.consul_and_hz_service import ConsulAndHazelcastService

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class FacadeService(ConsulAndHazelcastService):
    service_name: str = "facade-service"

    def __init__(self, port: int) -> None:
        super().__init__(self.service_name, port)
        self.tries = 10
        mq_name = self.consul_client.kv.get("message-queue")[1]['Value'].decode()
        self.hz_mq = self.hz_client.get_queue(mq_name)

    def select_random_service(self, service_name):
        """Choose in a way that repearts least possible amount of times"""
        # only those services which are alive and their agents are too, are selected.
        service = random.choice(list(filter(
            lambda x: all(check['Status'] == 'passing' for check in x['Checks']),
            self.consul_client.health.service(service_name)[1]
        )))
        ip = service['Service']['Address']
        port = service['Service']['Port']
        address = f"http://{ip}:{port}"
        logger.info(f"Selected {address}...")
        return address

    async def microservice_get(self, client, micro_name: str, path: str):
        """Get an address, retry 'self.tries' times"""
        logger.info(f"Getting {micro_name}/{path}...")
        for _ in range(self.tries):
            try:
                address = self.select_random_service(micro_name)
                response = await client.get(urljoin(address, path))
                if response.status_code == 200:
                    return response.json()
            except httpx.ConnectError as e:
                pass
            logger.info(f"Failed to GET: {address}")
        raise HTTPException(status_code=503, detail=f"Error when requesting {micro_name}: {response} (tried: {self.tries})")

    async def microservice_post(self, client, micro_name: str, path: str, json: dict):
        """Post JSON to an address, retry 'self.tries' times"""
        logger.info(f"Posting {json}...")
        for _ in range(self.tries):
            try:
                address = self.select_random_service(micro_name)
                response = await client.post(
                    urljoin(address, path), json=json,
                )
                if response.status_code == 200:
                    return response.json()
            except httpx.ConnectError as e:
                pass
            logger.info(f"Failed to POST: {address}")
        raise HTTPException(status_code=503, detail=f"Error when requesting {micro_name}: {response} (tried: {self.tries})")

    async def add_message(self, msg: str):
        async with httpx.AsyncClient() as client:
            await self.microservice_post(client, "logging-service", "log", Message(msg).json())
            self.hz_mq.offer(msg).result()

    async def get_messages(self):
        async with httpx.AsyncClient() as client:
            logging_resp = await self.microservice_get(client, "logging-service", "log")
            messages_resp = await self.microservice_get(client, "messages-service", "message")
        return logging_resp + ": " + str(messages_resp)
