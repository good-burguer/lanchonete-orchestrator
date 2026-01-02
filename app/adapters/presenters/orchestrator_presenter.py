from pydantic import BaseModel

class OrchestratorRunResponse(BaseModel):
    payment_code: str