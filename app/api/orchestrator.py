from fastapi import APIRouter
import asyncio
from app.services.http_client import async_request
from app.config import SERVICE_A_URL
from app.utils.debug import var_dump_die

router = APIRouter(prefix="/orchestrate", tags=["Orchestrator"])

@router.get("/")
async def root():
    return {"message": "Orchestrator is running!"}

@router.get("/run")
async def run_orchestration():
    service_a = f"{SERVICE_A_URL}/pagamento"
    
    results = await asyncio.gather(
        async_request("GET", service_a),
        return_exceptions=True,
    )

    return {
        "service_a": results[0]
    }
