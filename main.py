from __future__ import annotations

import asyncio
import io
import os
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import numpy as np
import soundfile as sf
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from loguru import logger

from fish_speech.utils.schema import ServeTTSRequest
from tools.server.model_manager import ModelManager

AMPLITUDE = 32768
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
MODEL_PATH = os.getenv("LLAMA_CHECKPOINT_PATH", "/app/checkpoints/s2-pro")
DECODER_PATH = os.getenv(
    "DECODER_CHECKPOINT_PATH", "/app/checkpoints/s2-pro/codec.pth"
)
DECODER_CONFIG = os.getenv("DECODER_CONFIG_NAME", "modded_dac_vq")
DEVICE = os.getenv("DEVICE", "cuda")
COMPILE = os.getenv("COMPILE", "0").lower() in {"1", "true", "yes", "on"}
HALF = os.getenv("HALF", "0").lower() in {"1", "true", "yes", "on"}
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "0"))


def _validate_request(req: ServeTTSRequest) -> None:
    if not req.text.strip():
        raise ValueError("text must not be empty")
    if MAX_TEXT_LENGTH > 0 and len(req.text) > MAX_TEXT_LENGTH:
        raise ValueError(f"text exceeds MAX_TEXT_LENGTH={MAX_TEXT_LENGTH}")
    if req.streaming and req.format != "wav":
        raise ValueError("streaming currently supports only WAV format")


def _iter_stream_chunks(req: ServeTTSRequest, engine) -> Iterator[bytes]:
    """Convert official engine events into one valid streamed WAV byte sequence.

    The engine emits a WAV header, zero or more PCM segments, and a final waveform.
    When segments were emitted, the final waveform duplicates those samples, so it is
    intentionally skipped. If no segments were emitted, the final waveform is encoded
    as a complete WAV fallback.
    """
    segment_count = 0
    sample_rate = engine.decoder_model.sample_rate

    for result in engine.inference(req):
        if result.code == "error":
            raise RuntimeError(str(result.error))

        if result.code == "header" and isinstance(result.audio, tuple):
            yield result.audio[1]
            continue

        if result.code == "segment" and isinstance(result.audio, tuple):
            segment_count += 1
            pcm = np.clip(result.audio[1], -1.0, 1.0)
            yield (pcm * AMPLITUDE).astype(np.int16).tobytes()
            continue

        if result.code == "final" and isinstance(result.audio, tuple):
            if segment_count == 0:
                buffer = io.BytesIO()
                sf.write(buffer, result.audio[1], sample_rate, format="WAV", subtype="PCM_16")
                yield buffer.getvalue()
            return

    if segment_count == 0:
        raise RuntimeError("No audio was generated")


def _generate_complete_audio(req: ServeTTSRequest, engine) -> bytes:
    sample_rate = engine.decoder_model.sample_rate
    final_audio = None
    collected_segments: list[np.ndarray] = []

    for result in engine.inference(req):
        if result.code == "error":
            raise RuntimeError(str(result.error))
        if result.code == "segment" and isinstance(result.audio, tuple):
            collected_segments.append(np.asarray(result.audio[1]))
        if result.code == "final" and isinstance(result.audio, tuple):
            final_audio = np.asarray(result.audio[1])
            break

    if final_audio is None:
        if not collected_segments:
            raise RuntimeError("No audio was generated")
        final_audio = np.concatenate(collected_segments)

    buffer = io.BytesIO()
    sf.write(buffer, final_audio, sample_rate, format=req.format.upper())
    return buffer.getvalue()


async def _async_stream(req: ServeTTSRequest, engine) -> AsyncIterator[bytes]:
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[bytes | BaseException | None] = asyncio.Queue()

    def producer() -> None:
        try:
            for chunk in _iter_stream_chunks(req, engine):
                loop.call_soon_threadsafe(queue.put_nowait, chunk)
        except BaseException as exc:
            loop.call_soon_threadsafe(queue.put_nowait, exc)
        finally:
            loop.call_soon_threadsafe(queue.put_nowait, None)

    producer_task = asyncio.create_task(asyncio.to_thread(producer))
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            if isinstance(item, BaseException):
                raise item
            yield item
    finally:
        await producer_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading Fish Speech S2 Pro from {}", MODEL_PATH)
    manager = await asyncio.to_thread(
        ModelManager,
        mode="tts",
        device=DEVICE,
        half=HALF,
        compile=COMPILE,
        llama_checkpoint_path=MODEL_PATH,
        decoder_checkpoint_path=DECODER_PATH,
        decoder_config_name=DECODER_CONFIG,
    )
    app.state.model_manager = manager
    app.state.inference_lock = asyncio.Lock()
    logger.info("Fish Speech model loaded; serving on {}:{}", HOST, PORT)
    yield
    logger.info("Shutting down Fish Speech server")


app = FastAPI(title="Fish Speech S2 Pro HTTP + WebSocket", lifespan=lifespan)


@app.get("/health")
@app.get("/v1/health")
async def health() -> JSONResponse:
    ready = hasattr(app.state, "model_manager")
    return JSONResponse(
        {
            "status": "ok" if ready else "loading",
            "model": "fishaudio/s2-pro",
            "http_tts": "/v1/tts",
            "websocket_tts": "/ws/tts",
            "port": PORT,
        },
        status_code=200 if ready else 503,
    )


@app.post("/v1/tts")
async def http_tts(req: ServeTTSRequest):
    try:
        _validate_request(req)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    engine = app.state.model_manager.tts_inference_engine

    if req.streaming:
        async def locked_stream() -> AsyncIterator[bytes]:
            async with app.state.inference_lock:
                async for chunk in _async_stream(req, engine):
                    yield chunk

        return StreamingResponse(
            locked_stream(),
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=audio.wav"},
        )

    try:
        async with app.state.inference_lock:
            audio = await asyncio.to_thread(_generate_complete_audio, req, engine)
    except Exception as exc:
        logger.exception("HTTP TTS failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    media_types = {
        "wav": "audio/wav",
        "mp3": "audio/mpeg",
        "opus": "audio/ogg",
        "pcm": "application/octet-stream",
    }
    return StreamingResponse(
        iter([audio]),
        media_type=media_types.get(req.format, "application/octet-stream"),
        headers={"Content-Disposition": f"attachment; filename=audio.{req.format}"},
    )


@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket) -> None:
    await websocket.accept()
    request_id = str(uuid.uuid4())

    try:
        payload = await websocket.receive_json()
        payload["streaming"] = True
        payload["format"] = "wav"
        req = ServeTTSRequest.model_validate(payload)
        _validate_request(req)

        engine = app.state.model_manager.tts_inference_engine
        await websocket.send_json(
            {
                "type": "accepted",
                "request_id": request_id,
                "sample_rate": engine.decoder_model.sample_rate,
                "format": "wav",
            }
        )

        started = time.perf_counter()
        first_chunk = True
        chunk_count = 0
        byte_count = 0

        async with app.state.inference_lock:
            async for chunk in _async_stream(req, engine):
                if first_chunk:
                    first_chunk = False
                    await websocket.send_json(
                        {
                            "type": "ttfa",
                            "request_id": request_id,
                            "ttfa_ms": round((time.perf_counter() - started) * 1000, 2),
                        }
                    )
                await websocket.send_bytes(chunk)
                chunk_count += 1
                byte_count += len(chunk)

        await websocket.send_json(
            {
                "type": "done",
                "request_id": request_id,
                "elapsed_ms": round((time.perf_counter() - started) * 1000, 2),
                "chunks": chunk_count,
                "bytes": byte_count,
            }
        )
        await websocket.close(code=1000)

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected: {}", request_id)
    except Exception as exc:
        logger.exception("WebSocket TTS failed")
        try:
            await websocket.send_json(
                {"type": "error", "request_id": request_id, "message": str(exc)}
            )
            await websocket.close(code=1011)
        except Exception:
            pass


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, workers=1, log_level="info")
