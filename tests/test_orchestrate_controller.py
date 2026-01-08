import pytest
from types import SimpleNamespace

from app.controller.orchestrate import OrchestrateController


@pytest.mark.asyncio
async def test_obtain_client_id_found(monkeypatch):
    async def fake_async_request(method, url, **kwargs):
        return {"data": {"id": 123}}

    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)

    controller = OrchestrateController()
    client_id = await controller.obtain_client_id(11122233344)

    assert client_id == 123


@pytest.mark.asyncio
async def test_obtain_client_id_not_found(monkeypatch):
    async def fake_async_request(method, url, **kwargs):
        return {"data": None}

    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)

    controller = OrchestrateController()
    client_id = await controller.obtain_client_id(11122233344)

    assert client_id == 0


@pytest.mark.asyncio
async def test_create_order_and_payment(monkeypatch):
    async def fake_async_request_order(method, url, **kwargs):
        if "pedidos" in url:
            return {"data": {"id": 10}}
        if "pagamento" in url:
            return {"data": {"codigo_pagamento": "ABC123"}}

    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request_order)

    controller = OrchestrateController()
    order_id = await controller.create_order({"cliente_id": 1, "produtos": [1, 2]})
    payment_code = await controller.create_payment({"pedido_id": order_id})

    assert order_id == 10
    assert payment_code == "ABC123"


@pytest.mark.asyncio
async def test_update_payment_status(monkeypatch):
    async def fake_async_request(method, url, **kwargs):
        return {"status": "PAID"}

    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_async_request)

    controller = OrchestrateController()
    payload = SimpleNamespace(payment_code="X1Y2", status=1)
    status = await controller.update_payment_status(payload)

    assert status == "PAID"


@pytest.mark.asyncio
async def test_debug_endpoint_raises(monkeypatch):
    # var_dump_die raises HTTPException; controller wraps and re-raises as Exception
    def fake_var_dump(data):
        raise Exception("debug")

    monkeypatch.setattr("app.controller.orchestrate.var_dump_die", fake_var_dump)

    controller = OrchestrateController()
    with pytest.raises(Exception):
        await controller.debug_endpoint()
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
