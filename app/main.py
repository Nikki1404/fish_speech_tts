import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any

import httpx
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from pydantic import ValidationError

from app.config import get_settings
from app.schemas import TTSRequest

settings = get_settings()
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("fish-ws-gateway")


def _timeout() -> httpx.Timeout:
    return httpx.Timeout(
        connect=settings.upstream_connect_timeout,
        read=settings.upstream_read_timeout,
        write=60.0,
        pool=30.0,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = httpx.AsyncClient(timeout=_timeout())
    try:
        yield
    finally:
        await app.state.http.aclose()


app = FastAPI(
    title="Fish Speech S2 Pro WebSocket Gateway",
    version="2.0.0",
    lifespan=lifespan,
)


def _authorized(websocket: WebSocket) -> bool:
    if not settings.ws_api_key:
        return True

    query_key = websocket.query_params.get("api_key", "")
    auth_header = websocket.headers.get("authorization", "")
    bearer = ""
    if auth_header.lower().startswith("bearer "):
        bearer = auth_header[7:].strip()

    return query_key == settings.ws_api_key or bearer == settings.ws_api_key


async def _send_json_safe(websocket: WebSocket, payload: dict[str, Any]) -> None:
    try:
        await websocket.send_json(payload)
    except (RuntimeError, WebSocketDisconnect):
        pass


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "service": "Fish Speech S2 Pro WebSocket Gateway",
        "websocket": "/ws/tts",
        "health": "/health",
        "protocol": "Send one JSON TTS request; receive JSON events and binary WAV chunks.",
    }


@app.get("/health")
async def health() -> dict[str, Any]:
    upstream_ok = False
    upstream_error: str | None = None

    try:
        response = await app.state.http.get(
            f"{settings.fish_http_url.rstrip('/')}/v1/health",
            timeout=httpx.Timeout(5.0),
        )
        upstream_ok = response.is_success
        if not upstream_ok:
            upstream_error = f"HTTP {response.status_code}"
    except Exception as exc:  # health endpoint must always return structured JSON
        upstream_error = str(exc)

    return {
        "status": "ok" if upstream_ok else "degraded",
        "gateway": True,
        "fish_speech": upstream_ok,
        "fish_speech_error": upstream_error,
    }


@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket) -> None:
    await websocket.accept()

    if not _authorized(websocket):
        await websocket.send_json({"type": "error", "message": "Unauthorized"})
        await websocket.close(code=4401, reason="Unauthorized")
        return

    request_id = uuid.uuid4().hex
    started = time.perf_counter()
    bytes_sent = 0
    chunks_sent = 0
    ttfa_ms: float | None = None

    try:
        raw_request = await websocket.receive_json()
        request = TTSRequest.model_validate(raw_request)

        if len(request.text) > settings.max_text_length:
            raise ValueError(
                f"Text length {len(request.text)} exceeds gateway limit "
                f"{settings.max_text_length}."
            )

        payload = request.model_dump(exclude_none=True)
        # The current Fish Speech self-hosted API only permits WAV for streaming.
        if request.streaming:
            payload["format"] = "wav"

        await websocket.send_json(
            {
                "type": "accepted",
                "request_id": request_id,
                "streaming": request.streaming,
                "format": payload["format"],
            }
        )

        url = f"{settings.fish_http_url.rstrip('/')}/v1/tts"
        async with app.state.http.stream(
            "POST",
            url,
            json=payload,
            headers={"Accept": "audio/wav"},
        ) as response:
            if not response.is_success:
                error_bytes = await response.aread()
                error_text = error_bytes.decode("utf-8", errors="replace")
                raise RuntimeError(
                    f"Fish Speech returned HTTP {response.status_code}: {error_text[:2000]}"
                )

            await websocket.send_json(
                {
                    "type": "metadata",
                    "request_id": request_id,
                    "content_type": response.headers.get("content-type", "audio/wav"),
                }
            )

            async for chunk in response.aiter_bytes(chunk_size=64 * 1024):
                if not chunk:
                    continue

                if ttfa_ms is None:
                    ttfa_ms = (time.perf_counter() - started) * 1000.0
                    await websocket.send_json(
                        {
                            "type": "ttfa",
                            "request_id": request_id,
                            "ttfa_ms": round(ttfa_ms, 2),
                        }
                    )

                await websocket.send_bytes(chunk)
                chunks_sent += 1
                bytes_sent += len(chunk)

        elapsed_ms = (time.perf_counter() - started) * 1000.0
        await websocket.send_json(
            {
                "type": "done",
                "request_id": request_id,
                "elapsed_ms": round(elapsed_ms, 2),
                "ttfa_ms": round(ttfa_ms, 2) if ttfa_ms is not None else None,
                "chunks": chunks_sent,
                "bytes": bytes_sent,
            }
        )
        await websocket.close(code=status.WS_1000_NORMAL_CLOSURE)

    except ValidationError as exc:
        await _send_json_safe(
            websocket,
            {
                "type": "error",
                "request_id": request_id,
                "message": "Invalid TTS request",
                "details": exc.errors(include_url=False),
            },
        )
        await websocket.close(code=4400, reason="Invalid request")
    except ValueError as exc:
        await _send_json_safe(
            websocket,
            {"type": "error", "request_id": request_id, "message": str(exc)},
        )
        await websocket.close(code=4400, reason="Invalid request")
    except WebSocketDisconnect:
        logger.info("Client disconnected: request_id=%s", request_id)
    except asyncio.CancelledError:
        logger.info("Request cancelled: request_id=%s", request_id)
        raise
    except Exception as exc:
        logger.exception("TTS request failed: request_id=%s", request_id)
        await _send_json_safe(
            websocket,
            {
                "type": "error",
                "request_id": request_id,
                "message": str(exc),
            },
        )
        try:
            await websocket.close(code=1011, reason="TTS generation failed")
        except RuntimeError:
            pass
