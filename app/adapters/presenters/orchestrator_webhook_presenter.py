from pydantic import BaseModel

class OrchestratorWebhookResponse(BaseModel):
    order_status: str