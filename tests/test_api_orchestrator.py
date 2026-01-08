from fastapi.testclient import TestClient
import pytest

from app.infrastructure.api.fastapi import app as fastapi_app


@pytest.fixture
def client():
    return TestClient(fastapi_app)


def test_run_orchestration_success(monkeypatch, client):
    async def fake_obtain(self, cpf):
        return 1

    async def fake_create_order(self, payload):
        return 2

    async def fake_create_payment(self, payload):
        return "PAY123"

    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.obtain_client_id", fake_obtain)
    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.create_order", fake_create_order)
    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.create_payment", fake_create_payment)

    resp = client.post("/orchestrate/run", json={"cpf": 12345678900, "produtos": [1, 2]})
    assert resp.status_code == 201
    assert resp.json().get("payment_code") == "PAY123"


def test_run_webhook_success(monkeypatch, client):
    async def fake_update(self, payload):
        return "PAID"

    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.update_payment_status", fake_update)

    resp = client.post("/orchestrate/run-webhook", json={"payment_code": "X", "status": 1})
    assert resp.status_code == 200
    assert resp.json().get("order_status") == "PAID"


def test_create_costumer_and_product_api(monkeypatch, client):
    async def fake_create_costumer(self, payload):
        return 77

    async def fake_create_product(self, payload):
        return 88

    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.create_costumer", fake_create_costumer)
    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.create_product", fake_create_product)

    # payload must satisfy ClienteCreateSchema: nome, email, cpf
    resp_c = client.post("/orchestrate/costumer", json={"nome": "Teste Cliente", "email": "a@b.com", "cpf": "12345678901"})
    assert resp_c.status_code == 201
    assert resp_c.json().get("costumer_id") == 77

    # payload must satisfy ProdutoCreateSchema: nome, categoria, preco
    resp_p = client.post("/orchestrate/product", json={"nome": "Produto X", "categoria": 1, "preco": 9.99})
    assert resp_p.status_code == 201
    assert resp_p.json().get("product_id") == 88


def test_run_orchestration_error_returns_400(monkeypatch, client):
    async def bad_obtain(cpf):
        raise Exception("fail")

    monkeypatch.setattr("app.api.orchestrator.OrchestrateController.obtain_client_id", bad_obtain)

    resp = client.post("/orchestrate/run", json={"cpf": 1, "produtos": []})
    assert resp.status_code == 400
