import threading
from fastapi import FastAPI
from .service import HzMessageProcessingService

app = FastAPI()

mp_service = HzMessageProcessingService()

consumer_thread = threading.Thread(target=mp_service.consume_messages)

@app.get("/message")
async def get_message():
    return mp_service.get_messages()

@app.on_event("startup")
async def startup_event():
    consumer_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    if consumer_thread.is_alive():
        mp_service.stop_consuming()
        consumer_thread.join()

@app.get("/message")
async def get_message():
    return mp_service.get_messages()
