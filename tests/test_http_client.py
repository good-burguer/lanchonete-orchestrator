import pytest
import httpx

from app.services import http_client


class FakeResponse:
    def __init__(self, status_code=200, json_data=None, text=""):
        self.status_code = status_code
        self._json = json_data or {}
        self.text = text

    def raise_for_status(self):
        if self.status_code >= 400:
            request = httpx.Request("GET", "http://test")
            raise httpx.HTTPStatusError("err", request=request, response=httpx.Response(self.status_code, content=self.text.encode()))

    def json(self):
        return self._json


class FakeAsyncClient:
    def __init__(self, timeout=None, raise_exc=None, response=None):
        self._raise_exc = raise_exc
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def request(self, method, url, **kwargs):
        if self._raise_exc:
            raise self._raise_exc
        return self._response


@pytest.mark.asyncio
async def test_async_request_success(monkeypatch):
    fake_resp = FakeResponse(status_code=200, json_data={"ok": True})

    def fake_client(*args, **kwargs):
        return FakeAsyncClient(response=fake_resp)

    monkeypatch.setattr(http_client.httpx, "AsyncClient", fake_client)

    result = await http_client.async_request("GET", "http://test")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_async_request_request_error(monkeypatch):
    exc = httpx.RequestError("connection failed")

    def fake_client(*args, **kwargs):
        return FakeAsyncClient(raise_exc=exc)

    monkeypatch.setattr(http_client.httpx, "AsyncClient", fake_client)

    result = await http_client.async_request("GET", "http://test")
    assert "error" in result and result["error"].startswith("Request failed")


@pytest.mark.asyncio
async def test_async_request_http_status_error(monkeypatch):
    response = httpx.Response(500, content=b'server error')
    request = httpx.Request("GET", "http://test")
    exc = httpx.HTTPStatusError("err", request=request, response=response)

    def fake_client(*args, **kwargs):
        return FakeAsyncClient(raise_exc=exc)

    monkeypatch.setattr(http_client.httpx, "AsyncClient", fake_client)

    result = await http_client.async_request("GET", "http://test")
    assert result.get("error") == "HTTP 500"
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
