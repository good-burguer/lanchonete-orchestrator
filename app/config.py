import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_PRODUCTION_URL = "http://lanchonete-producao"
SERVICE_ORDER_URL = "http://lanchonete-pedidos"
SERVICE_PAYMENT_URL = "http://lanchonete-pagamento"

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 100))
