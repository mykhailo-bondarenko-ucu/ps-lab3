import sys
import httpx
import random
import logging
import logging.config
from .message import Message
from urllib.parse import urljoin
from fastapi import HTTPException

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

class FacadeService:
    def __init__(self) -> None:
        self.micro_config = {
            "logging-service": [["http://localhost:8082", "http://localhost:8083", "http://localhost:8084"], 0],
            "messages-service": [["http://localhost:8085"], 0]
        }
        self.tries = 10
    
    def select_random_service(self, service_name):
        """Choose in a way that repearts least possible amount of times"""
        service_list, i = self.micro_config[service_name]
        if i >= len(service_list):
            random.shuffle(service_list)
            i = 0
        address = service_list[i]
        i += 1
        self.micro_config[service_name] = [service_list, i]
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

    async def get_messages(self):
        async with httpx.AsyncClient() as client:
            logging_resp = await self.microservice_get(client, "logging-service", "log")
            messages_resp = await self.microservice_get(client, "messages-service", "message")
        return logging_resp + ": " + messages_resp
