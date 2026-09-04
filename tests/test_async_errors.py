"""Async error-path tests: failed responses must raise, never return None."""

import httpx
import pytest

from fastpix_python import Fastpix, errors, models


def _sdk(status: int, body: str):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=body, headers={"content-type": "application/json"})

    return Fastpix(
        security=models.Security(username="u", password="p"),
        async_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )


@pytest.mark.asyncio
async def test_async_4xx_raises_typed_error():
    sdk = _sdk(404, '{"success":false,"error":{"code":404,"message":"not found"}}')
    with pytest.raises(errors.FastpixError):
        await sdk.live_playback.get_live_stream_playback_id_async(stream_id="s", playback_id="p")


@pytest.mark.asyncio
async def test_async_5xx_raises_default_error():
    sdk = _sdk(500, "boom")
    with pytest.raises(errors.FastpixDefaultError):
        await sdk.live_playback.update_live_stream_domain_restrictions_async(
            stream_id="s", playback_id="p", default_policy="deny", allow=["example.com"]
        )


def test_sync_4xx_raises_for_parity():
    sdk = _sdk(403, '{"success":false,"error":{"code":403,"message":"forbidden"}}')
    with pytest.raises(errors.FastpixError):
        sdk.live_playback.update_live_stream_user_agent_restrictions(
            stream_id="s", playback_id="p", deny=["PostmanRuntime/7.29.0"]
        )
