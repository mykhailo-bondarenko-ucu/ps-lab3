import uuid

class Message:
    def __init__(self, msg) -> None:
        self.msg = msg
        self.uuid = str(uuid.uuid4())

    def json(self):
        return {"text": self.msg, "uuid": self.uuid}