from pydantic import BaseModel


class RequestModel(BaseModel):
    def to_create_model(self):
        raise NotImplementedError("This method has to be implemented on inherited models")
