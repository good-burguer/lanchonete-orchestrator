from app.infrastructure.api.fastapi import app, Depends
from app.api import orchestrator

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(orchestrator.router)