import pytest
from types import SimpleNamespace
from fastapi import HTTPException

from app.controller.orchestrate import OrchestrateController
from app.utils import debug as debug_module


@pytest.mark.asyncio
async def test_obtain_client_id_exception(monkeypatch):
    # make async_request raise, gather will return exception -> controller should raise
    async def bad_request(method, url, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.controller.orchestrate.async_request", bad_request)

    controller = OrchestrateController()
    with pytest.raises(Exception) as exc:
        await controller.obtain_client_id(123)

    assert "Orchestration failed" in str(exc.value)


@pytest.mark.asyncio
async def test_create_order_failure_raises(monkeypatch):
    async def bad_request(method, url, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.controller.orchestrate.async_request", bad_request)

    controller = OrchestrateController()
    with pytest.raises(Exception) as exc:
        await controller.create_order({"cliente_id": 1, "produtos": []})

    assert "Order creation failed" in str(exc.value)


@pytest.mark.asyncio
async def test_create_payment_failure_raises(monkeypatch):
    async def bad_request(method, url, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.controller.orchestrate.async_request", bad_request)

    controller = OrchestrateController()
    with pytest.raises(Exception) as exc:
        await controller.create_payment({"pedido_id": 1})

    assert "Payment creation failed" in str(exc.value)


@pytest.mark.asyncio
async def test_create_costumer_and_product_success(monkeypatch):
    async def fake_request(method, url, **kwargs):
        return {"data": {"id": 55}}

    monkeypatch.setattr("app.controller.orchestrate.async_request", fake_request)

    controller = OrchestrateController()
    # payloads that expose model_dump
    class P:
        def model_dump(self):
            return {"nome": "x"}

    cid = await controller.create_costumer(P())
    pid = await controller.create_product(P())

    assert cid == 55
    assert pid == 55


def test_var_dump_die_raises_and_payload(capsys):
    # call var_dump_die and assert it raises HTTPException and payload structure
    data = {"a": 1}
    with pytest.raises(HTTPException) as exc:
        debug_module.var_dump_die(data)

    # check detail payload
    detail = exc.value.detail
    assert detail.get("debug") is True
    assert "location" in detail
    assert detail.get("data") == data


def test_main_health_import_and_call():
    # import app.main and call health_check
    from app import main as m

    assert hasattr(m, "health_check")
    assert m.health_check() == {"status": "ok"}
