from fastapi import APIRouter, HTTPException, status
from app.adapters.dto.pagamento_webhook_dto import PagamentoAtualizaWebhookSchema
from app.utils.debug import var_dump_die
from app.controller.orchestrate import OrchestrateController

router = APIRouter(prefix="/orchestrate", tags=["Orchestrator"])

@router.get("/")
async def root():
    return {"message": "Orchestrator is running!"}

@router.post("/run")
async def run_orchestration(payload_data: dict):
    try:
        client_id = await OrchestrateController().obtain_client_id(payload_data)
        order_id = await OrchestrateController().create_order({"cliente_id": client_id, "produtos": payload_data.get("produtos")})
        payment_code = await OrchestrateController().create_payment({"pedido_id": order_id})

        return {
            "payment_response": payment_code
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post('/run-webhook')
async def run_webhook_orchestration(payment_data: PagamentoAtualizaWebhookSchema):
    try:
        webhook_result = await OrchestrateController().update_payment_status(payment_data)
        
        return {
            "webhook_response": webhook_result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/costumer")
async def create_costumer(payload_data: dict):
    try:
        costumer_id = await OrchestrateController().create_costumer(payload_data)

        return {
            "costumer_response": costumer_id
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/product")
async def create_product(payload_data: dict):
    try:
        product_id = await OrchestrateController().create_product(payload_data)

        return {
            "product_response": product_id
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/debug")
async def debug():
    try:
        await OrchestrateController().debug_endpoint()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))