import asyncio
from app.services.http_client import async_request
from app.config import SERVICE_PRODUCTION_URL, SERVICE_ORDER_URL, SERVICE_PAYMENT_URL

from app.utils.debug import var_dump_die

class OrchestrateController:
    
    def __init__(self):
        pass
    
    async def obtain_client_id(self, cpf: int):
        try:    
            if cpf is not None:                
                response = await asyncio.gather(
                    async_request("GET", f"{SERVICE_PRODUCTION_URL}/clientes/cpf/{cpf}"),
                    return_exceptions=True,
                )
                result_data = response[0]
                
                if result_data.get('data') is not None:
                    client_id = result_data['data'].get('id')
                    
                    return client_id
                else:
                    return 0
        except Exception as e:
            raise Exception(f"Orchestration failed: {str(e)}")
        
    async def create_order(self, order_payload: dict):
        try:
            response = await asyncio.gather(
                async_request("POST", f"{SERVICE_ORDER_URL}/pedidos/", json=order_payload),
                return_exceptions=True,
            )
            result_data = response[0]
            
            return result_data.get('data').get('id')
        except Exception as e:
            raise Exception(f"Order creation failed: {str(e)}")
        
    async def create_payment(self, payment_payload: dict):
        try:
            response = await asyncio.gather(
                async_request("POST", f"{SERVICE_PAYMENT_URL}/pagamento/", json=payment_payload),
                return_exceptions=True,
            )
            var_dump_die(response)
            result_data = response[0]

            return result_data.get('data').get('codigo_pagamento')
        except Exception as e:
            raise Exception(f"Payment creation failed: {str(e)}")

    async def update_payment_status(self, payment_update_payload: dict):
        try:
            webhook_payload = {
                "codigo_pagamento": payment_update_payload.payment_code,
                "status": payment_update_payload.status
            }
            webhook_result = await asyncio.gather(
                async_request("POST", f"{SERVICE_PAYMENT_URL}/webhook/update-payment", json=webhook_payload),
                return_exceptions=True,
            )
            result_data = webhook_result[0]
            
            return result_data.get('status')
        except Exception as e:
            raise Exception(f"Payment update failed: {str(e)}")
        
    async def create_costumer(self, customer_payload: dict):
        try:
            response = await asyncio.gather(
                async_request("POST", f"{SERVICE_PRODUCTION_URL}/clientes/", json=customer_payload.model_dump()),
                return_exceptions=True,
            )
            result_data = response[0]
            
            return result_data.get('data').get('id')
        except Exception as e:
            raise Exception(f"Orchestration failed: {str(e)}")
        
    async def create_product(self, product_payload: dict):
        try:    
            response = await asyncio.gather(
                async_request("POST", f"{SERVICE_PRODUCTION_URL}/produtos/", json=product_payload.model_dump()),
                return_exceptions=True,
            )
            result_data = response[0]
            
            return result_data.get('data').get('id')
        except Exception as e:
            raise Exception(f"Orchestration failed: {str(e)}")
        
    async def debug_endpoint(self):
        try:
            var_dump_die(
                f"PRODUCTION: {SERVICE_PRODUCTION_URL}\n"f"ORDER: {SERVICE_ORDER_URL}\n"f"PAYMENT: {SERVICE_PAYMENT_URL}"
            )
        except Exception as e:
            raise Exception(f"Orchestration failed: {str(e)}")