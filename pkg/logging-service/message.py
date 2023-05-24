from pydantic import BaseModel

class MessageBody(BaseModel):
    text: str
    uuid: str