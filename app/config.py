import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://payment_app:8080")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 100))
