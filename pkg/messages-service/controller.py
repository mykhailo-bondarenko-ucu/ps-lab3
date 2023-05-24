import uvicorn
import threading
from fastapi import FastAPI
from .service import HzMessageProcessingService
from ..base.helpers import setup_and_parse_args

args = setup_and_parse_args()

app = FastAPI()

mp_service = HzMessageProcessingService(args.port)

consumer_thread = threading.Thread(target=mp_service.consume_messages)

@app.on_event("startup")
async def startup_event():
    mp_service.register_service()

@app.on_event("shutdown")
async def shutdown_event():
    mp_service.deregister_and_shutdown()

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

@app.get("/health")
async def check_health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(f"pkg.{mp_service.service_name}.controller:app", port=args.port, reload=True)
