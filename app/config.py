import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_PRODUCTION_URL = os.getenv("SERVICE_PRODUCTION_URL")
SERVICE_ORDER_URL = os.getenv("SERVICE_ORDER_URL")
SERVICE_PAYMENT_URL = os.getenv("SERVICE_PAYMENT_URL")

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 100))
