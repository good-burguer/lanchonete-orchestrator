from fastapi import APIRouter, HTTPException, status
import asyncio
from app.services.http_client import async_request
from app.config import SERVICE_A_URL
from app.adapters.dto.pagamento_webhook_dto import PagamentoAtualizaWebhookSchema
from app.utils.debug import var_dump_die

router = APIRouter(prefix="/orchestrate", tags=["Orchestrator"])

@router.get("/")
async def root():
    return {"message": "Orchestrator is running!"}

@router.post("/run")
async def run_orchestration():
    try:
        payment_payload = {
            "pedido_id": 1
        }
        
        payment_service_result = await asyncio.gather(
            async_request("POST", f"{SERVICE_A_URL}/pagamento/", json=payment_payload),
            return_exceptions=True,
        )
        
        return {
            "payment_response": payment_service_result[0]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post('/run-webhook')
async def run_webhook_orchestration(payment_data: PagamentoAtualizaWebhookSchema):
    try:
        webhook_payload = {
            "codigo_pagamento": payment_data.payment_code,
            "status": payment_data.status
        }
        
        webhook_result = await asyncio.gather(
            async_request("POST", f"{SERVICE_A_URL}/webhook/update-payment", json=webhook_payload),
            return_exceptions=True,
        )

        return {
            "webhook_response": webhook_result[0]
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))