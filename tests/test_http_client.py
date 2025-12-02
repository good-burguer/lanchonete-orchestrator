import pytest
import httpx
import types
from app.services.http_client import async_request


class DummyResponse:
    def __init__(self, payload=None, status_code=200, text=""):
        self._payload = payload or {}
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("err", request=None, response=self)


class DummyClientSuccess:
    def __init__(self, timeout=None):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def request(self, method, url, **kwargs):
        return DummyResponse({"data": {"id": 1}}, status_code=200)


class DummyClientRequestError:
    def __init__(self, timeout=None):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def request(self, method, url, **kwargs):
        raise httpx.RequestError("failed")


@pytest.mark.asyncio
async def test_async_request_success(monkeypatch):
    monkeypatch.setattr("app.services.http_client.httpx.AsyncClient", DummyClientSuccess)

    resp = await async_request("GET", "http://example")
    assert isinstance(resp, dict)
    assert "data" in resp


@pytest.mark.asyncio
async def test_async_request_request_error(monkeypatch):
    monkeypatch.setattr("app.services.http_client.httpx.AsyncClient", DummyClientRequestError)

    resp = await async_request("GET", "http://example")
    assert isinstance(resp, dict)
    assert "error" in resp
