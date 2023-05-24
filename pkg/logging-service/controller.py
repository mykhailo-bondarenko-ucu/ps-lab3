import sys
import uvicorn
import logging
import logging.config
from fastapi import FastAPI
from .message import MessageBody
from .service import HazelCastLoggingService
from ..base.helpers import setup_and_parse_args

args = setup_and_parse_args()

app = FastAPI()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

logging_service = HazelCastLoggingService(args.port)

@app.on_event("startup")
async def startup_event():
    logging_service.register_service()

@app.on_event("shutdown")
async def shutdown_event():
    logging_service.deregister_and_shutdown()

@app.get("/log")
async def list_log():
    resp = f'[{", ".join(logging_service.get_messages())}]'
    logger.info(f"Response: {resp}")
    return resp

@app.post("/log")
async def post_message(message: MessageBody):
    logger.info(f"Message{{{message}}}")
    logging_service.add_message(message)

@app.get("/health")
async def check_health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(f"pkg.{logging_service.service_name}.controller:app", port=args.port, reload=True)
