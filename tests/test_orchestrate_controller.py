import pytest
import asyncio
from app.controller.orchestrate import OrchestrateController


async def fake_async_request(method: str, url: str, **kwargs):
    if "/clientes/cpf/" in url:
        return {"data": {"id": 42}}
    if "/pedidos/" in url:
        return {"data": {"id": 100}}
    if "/pagamento/" in url and "webhook" not in url:
        return {"data": {"codigo_pagamento": "PAY123"}}
    if "webhook" in url:
        return {"status": "ok"}


@pytest.mark.asyncio
async def test_obtain_client_id(monkeypatch):
    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)
    controller = OrchestrateController()

    client_id = await controller.obtain_client_id({"cpf": "1234"})
    assert client_id == 42


@pytest.mark.asyncio
async def test_create_order_and_payment(monkeypatch):
    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)
    controller = OrchestrateController()

    order_id = await controller.create_order({"cliente_id": 42, "produtos": []})
    assert order_id == 100

    payment_code = await controller.create_payment({"pedido_id": order_id})
    assert payment_code == "PAY123"


@pytest.mark.asyncio
async def test_update_payment_status(monkeypatch):
    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)
    controller = OrchestrateController()

    class Payload:
        payment_code = "PAY123"
        status = 1

    result = await controller.update_payment_status(Payload)
    assert result == "ok"
