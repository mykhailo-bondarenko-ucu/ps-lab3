import logging
import logging.config
from .service import FacadeService
from fastapi import FastAPI, Request

app = FastAPI()

facade_service = FacadeService()

@app.post("/facade_service")
async def facade_service_post(request: Request):
    msg = (await request.body()).decode().strip('"')
    await facade_service.add_message(msg)

@app.get("/facade_service")
async def facade_service_get():
    return await facade_service.get_messages()
