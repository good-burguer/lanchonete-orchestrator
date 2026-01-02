from pydantic import BaseModel

class ProdutoResponse(BaseModel):
    product_id: int