from pydantic import BaseModel

class ClienteResponse(BaseModel):
    costumer_id: int
