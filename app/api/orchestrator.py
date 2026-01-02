from fastapi import APIRouter, HTTPException, status

from app.adapters.dto.pagamento_webhook_dto import PagamentoAtualizaWebhookDTO
from app.controller.orchestrate import OrchestrateController

from app.adapters.presenters.cliente_presenter import ClienteResponse
from app.adapters.presenters.produto_presenter import ProdutoResponse
from app.adapters.dto.cliente_dto import ClienteCreateSchema
from app.adapters.dto.produto_dto import ProdutoCreateSchema
from app.adapters.presenters.orchestrator_presenter import OrchestratorRunResponse
from app.adapters.presenters.orchestrator_webhook_presenter import OrchestratorWebhookResponse
from app.adapters.dto.create_order_dto import CreateOrderDTO

from app.utils.debug import var_dump_die

router = APIRouter(prefix="/orchestrate", tags=["Orchestrator"])

@router.get("/")
async def root():
    return {"message": "Orchestrator is running!"}

@router.post("/run", response_model=OrchestratorRunResponse, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar o pedido"
                }
            }
        }
    }
})
async def run_orchestration(payload_data: CreateOrderDTO):
    try:
        client_id = await OrchestrateController().obtain_client_id(payload_data.cpf)
        order_id = await OrchestrateController().create_order({"cliente_id": client_id, "produtos": payload_data.produtos})
        payment_code = await OrchestrateController().create_payment({"pedido_id": order_id})

        return {
            "payment_code": payment_code
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post('/run-webhook', response_model=OrchestratorWebhookResponse, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao editar o pedido"
                }
            }
        }
    }
})
async def run_webhook_orchestration(payment_data: PagamentoAtualizaWebhookDTO):
    try:
        webhook_result = await OrchestrateController().update_payment_status(payment_data)
        
        return {
            "order_status": webhook_result
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/costumer", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar cliente"
                }
            }
        }
    }
})
async def create_costumer(payload_data: ClienteCreateSchema):
    try:

        return {
            "costumer_id": await OrchestrateController().create_costumer(payload_data)
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.post("/product", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED, responses={
    400: {
        "description": "Erro de validação",
        "content": {
            "application/json": {
                "example": {
                    "message": "Erro de integridade ao criar produto"
                }
            }
        }
    }
})
async def create_product(payload_data: ProdutoCreateSchema):
    try:

        return {
            "product_id": await OrchestrateController().create_product(payload_data)
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/debug")
async def debug():
    try:
        await OrchestrateController().debug_endpoint()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))