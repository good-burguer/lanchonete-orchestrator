from pydantic import BaseModel

class CreateOrderDTO(BaseModel):
    cpf: int
    produtos: list[int]