import uvicorn
from .service import FacadeService
from fastapi import FastAPI, Request
from ..base.helpers import setup_and_parse_args

args = setup_and_parse_args()

app = FastAPI()

facade_service = FacadeService(args.port)

@app.on_event("startup")
async def startup_event():
    facade_service.register_service()

@app.on_event("shutdown")
async def shutdown_event():
    facade_service.deregister_and_shutdown()

@app.post("/facade_service")
async def facade_service_post(request: Request):
    msg = (await request.body()).decode().strip('"')
    await facade_service.add_message(msg)

@app.get("/facade_service")
async def facade_service_get():
    return await facade_service.get_messages()

@app.get("/health")
async def check_health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(f"pkg.{facade_service.service_name}.controller:app", port=args.port, reload=True)
