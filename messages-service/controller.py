import threading
from fastapi import FastAPI
from .service import HzMessageProcessingService

app = FastAPI()

mp_service = HzMessageProcessingService()

@app.get("/message")
async def get_message():
    return mp_service.get_messages()

consumer_thread = threading.Thread(target=mp_service.consume_messages)

consumer_thread.start()

consumer_thread.join()
