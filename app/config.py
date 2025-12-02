import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_PRODUCTION_URL = os.getenv("SERVICE_PRODUCTION_URL", "http://production_app:8080")
SERVICE_ORDER_URL = os.getenv("SERVICE_ORDER_URL", "http://order_app:8080")
SERVICE_PAYMENT_URL = os.getenv("SERVICE_A_URL", "http://payment_app:8080")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 100))
