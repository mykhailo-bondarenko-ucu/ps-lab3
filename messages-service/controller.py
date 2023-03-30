import logging
import logging.config
from fastapi import FastAPI

app = FastAPI()

@app.get("/message")
async def get_message():
    return "messages-service is not implemented yet"
