from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_orchestrator_root():
    """
    Verifica se a rota raiz do orchestrator está respondendo corretamente.
    """
    response = client.get("/orchestrate/")

    assert response.status_code == 200
    assert response.json() == {"message": "Orchestrator is running!"}