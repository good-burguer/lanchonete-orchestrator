import httpx
from app.config import REQUEST_TIMEOUT
from app.utils.logger import logger
from app.utils.debug import var_dump_die

async def async_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()

            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Erro ao chamar {url}: {e}")

            return {"error": f"Request failed: {str(e)}"}
        except httpx.HTTPStatusError as e:
            logger.warning(f"Erro HTTP {e.response.status_code} em {url}")
            
            return {"error": f"HTTP {e.response.status_code}", "detail": e.response.text}
