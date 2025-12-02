from app.infrastructure.api.fastapi import app, Depends
from app.api import orchestrator

app.include_router(orchestrator.router)