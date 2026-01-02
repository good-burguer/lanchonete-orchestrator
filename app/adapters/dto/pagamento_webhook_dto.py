from pydantic import BaseModel
from app.adapters.enums.status_pagamento import PagamentoStatusEnum

class PagamentoAtualizaWebhookDTO(BaseModel):
    payment_code: str
    status: PagamentoStatusEnum