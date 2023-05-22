import sys
import logging
import logging.config
from fastapi import FastAPI
from .message import MessageBody
from .service import HazelCastLoggingService

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

messages = dict()

logging_service = HazelCastLoggingService()

@app.get("/log")
async def list_log():
    resp = f'[{", ".join(logging_service.get_messages())}]'
    logger.info(f"Response: {resp}")
    return resp

@app.post("/log")
async def post_message(message: MessageBody):
    logger.info(f"Message{{{message}}}")
    logging_service.add_message(message)
