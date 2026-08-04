from __future__ import annotations

import asyncio
import io
import os
import queue
import struct
import threading
import time
import uuid
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterator

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response, StreamingResponse
from loguru import logger
from pydantic import ValidationError

from fish_speech.utils.schema import ServeTTSRequest
from tools.server.model_manager import ModelManager


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

DEVICE = os.getenv("DEVICE", "cpu").strip().lower()

MODEL_PATH = os.getenv(
    "LLAMA_CHECKPOINT_PATH",
    "/app/checkpoints/s2-pro",
)

DECODER_PATH = os.getenv(
    "DECODER_CHECKPOINT_PATH",
    "/app/checkpoints/s2-pro/codec.pth",
)

DECODER_CONFIG = os.getenv(
    "DECODER_CONFIG_NAME",
    "modded_dac_vq",
)

MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "1000"))
PCM_SCALE = 32768


class ServerState:
    model_manager: ModelManager | None = None
    ready: bool = False
    startup_error: str | None = None


state = ServerState()

# Fish Speech uses shared model buffers. Process one request at a time.
inference_lock = threading.Lock()


def validate_environment() -> None:
    if DEVICE != "cpu":
        raise RuntimeError(
            f"This container is configured for CPU inference, "
            f"but DEVICE={DEVICE!r}"
        )


def get_engine():
    if not state.ready or state.model_manager is None:
        raise RuntimeError(
            state.startup_error or "Fish Speech model is not ready."
        )

    return state.model_manager.tts_inference_engine


def get_sample_rate(engine) -> int:
    decoder = engine.decoder_model

    if hasattr(decoder, "spec_transform"):
        return int(decoder.spec_transform.sample_rate)

    return int(decoder.sample_rate)


def validate_tts_request(request: ServeTTSRequest) -> None:
    text = request.text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    if MAX_TEXT_LENGTH > 0 and len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Text exceeds the maximum length of "
            f"{MAX_TEXT_LENGTH} characters."
        )

    if request.streaming and request.format != "wav":
        raise ValueError("Streaming mode supports WAV format only.")


def encode_audio(
    audio: np.ndarray,
    sample_rate: int,
    audio_format: str,
) -> bytes:
    audio = np.asarray(audio, dtype=np.float32)
    audio = np.clip(audio, -1.0, 1.0)

    if audio_format == "pcm":
        return (audio * PCM_SCALE).astype(np.int16).tobytes()

    if audio_format != "wav":
        raise ValueError(
            "This standalone CPU server currently supports WAV and PCM output."
        )

    buffer = io.BytesIO()

    sf.write(
        buffer,
        audio,
        sample_rate,
        format="WAV",
        subtype="PCM_16",
    )

    return buffer.getvalue()


def generate_complete_audio(
    request: ServeTTSRequest,
) -> tuple[bytes, int]:
    engine = get_engine()
    sample_rate = get_sample_rate(engine)

    final_audio: np.ndarray | None = None

    with inference_lock:
        for result in engine.inference(request):
            if result.code == "error":
                raise RuntimeError(str(result.error))

            if result.code == "final" and result.audio is not None:
                sample_rate, final_audio = result.audio

    if final_audio is None or final_audio.size == 0:
        raise RuntimeError("Fish Speech generated no audio.")

    encoded = encode_audio(
        final_audio,
        int(sample_rate),
        request.format,
    )

    return encoded, int(sample_rate)


def generate_streaming_chunks(
    request: ServeTTSRequest,
) -> Iterator[bytes]:
    """
    Return one WAV header followed by PCM16 audio segments.

    Fish Speech also emits a final concatenated waveform after streaming
    all segments. That final result is intentionally not sent again.
    """
    engine = get_engine()
    received_segment = False

    with inference_lock:
        for result in engine.inference(request):
            if result.code == "error":
                raise RuntimeError(str(result.error))

            if result.code == "header":
                if result.audio is None:
                    continue

                _, header = result.audio

                if isinstance(header, np.ndarray):
                    yield header.tobytes()
                else:
                    yield bytes(header)

            elif result.code == "segment":
                if result.audio is None:
                    continue

                _, audio = result.audio

                audio = np.asarray(audio, dtype=np.float32)
                audio = np.clip(audio, -1.0, 1.0)

                pcm = (audio * PCM_SCALE).astype(np.int16)

                received_segment = True
                yield pcm.tobytes()

            elif result.code == "final":
                # All segments were already returned.
                break

    if not received_segment:
        raise RuntimeError("Fish Speech generated no streaming audio.")


async def generate_streaming_chunks_async(
    request: ServeTTSRequest,
) -> AsyncIterator[bytes]:
    output_queue: queue.Queue[bytes | Exception | None] = queue.Queue(
        maxsize=8
    )

    def producer() -> None:
        try:
            for chunk in generate_streaming_chunks(request):
                output_queue.put(chunk)

        except Exception as exc:
            output_queue.put(exc)

        finally:
            output_queue.put(None)

    thread = threading.Thread(
        target=producer,
        name=f"fish-tts-{uuid.uuid4().hex[:8]}",
        daemon=True,
    )
    thread.start()

    while True:
        item = await asyncio.to_thread(output_queue.get)

        if item is None:
            break

        if isinstance(item, Exception):
            raise item

        yield item


@asynccontextmanager
async def lifespan(_: FastAPI):
    validate_environment()

    logger.info("Loading Fish Speech S2 Pro on CPU")
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Decoder path: {DECODER_PATH}")

    try:
        state.model_manager = await asyncio.to_thread(
            ModelManager,
            mode="tts",
            device="cpu",
            half=False,
            compile=False,
            llama_checkpoint_path=MODEL_PATH,
            decoder_checkpoint_path=DECODER_PATH,
            decoder_config_name=DECODER_CONFIG,
        )

        state.ready = True
        state.startup_error = None

        logger.info("Fish Speech S2 Pro loaded successfully on CPU")

    except Exception as exc:
        state.ready = False
        state.startup_error = str(exc)

        logger.exception(f"Model startup failed: {exc}")
        raise

    yield

    state.ready = False
    logger.info("Fish Speech server stopped")


app = FastAPI(
    title="Fish Speech S2 Pro CPU Server",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> dict:
    return {
        "service": "Fish Speech S2 Pro CPU Server",
        "device": DEVICE,
        "health": "/health",
        "http_tts": "/v1/tts",
        "websocket_tts": "/ws/tts",
        "docs": "/docs",
    }


@app.get("/health")
async def health() -> JSONResponse:
    response = {
        "status": "ok" if state.ready else "loading",
        "ready": state.ready,
        "device": DEVICE,
        "model": "fishaudio/s2-pro",
        "http_tts": "/v1/tts",
        "websocket_tts": "/ws/tts",
        "port": PORT,
        "startup_error": state.startup_error,
    }

    return JSONResponse(
        content=response,
        status_code=200 if state.ready else 503,
    )


@app.post("/v1/tts")
async def http_tts(request: ServeTTSRequest):
    try:
        validate_tts_request(request)

        if not state.ready:
            raise HTTPException(
                status_code=503,
                detail=state.startup_error or "Model is still loading.",
            )

        if request.streaming:
            stream_request = request.model_copy(
                update={
                    "streaming": True,
                    "format": "wav",
                }
            )

            return StreamingResponse(
                generate_streaming_chunks_async(stream_request),
                media_type="audio/wav",
                headers={
                    "Content-Disposition": (
                        'attachment; filename="speech.wav"'
                    ),
                    "Cache-Control": "no-store",
                },
            )

        audio_bytes, sample_rate = await asyncio.to_thread(
            generate_complete_audio,
            request,
        )

        content_type = (
            "audio/wav"
            if request.format == "wav"
            else "application/octet-stream"
        )

        extension = "wav" if request.format == "wav" else "pcm"

        return Response(
            content=audio_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": (
                    f'attachment; filename="speech.{extension}"'
                ),
                "X-Audio-Sample-Rate": str(sample_rate),
                "Cache-Control": "no-store",
            },
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        logger.exception(f"HTTP TTS failed: {exc}")

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.websocket("/ws/tts")
async def websocket_tts(websocket: WebSocket) -> None:
    await websocket.accept()

    request_id = str(uuid.uuid4())
    started_at = time.perf_counter()

    first_audio_at: float | None = None
    chunks_sent = 0
    bytes_sent = 0

    try:
        if not state.ready:
            await websocket.send_json(
                {
                    "type": "error",
                    "request_id": request_id,
                    "message": (
                        state.startup_error or "Model is still loading."
                    ),
                }
            )
            await websocket.close(code=1013)
            return

        payload = await websocket.receive_json()

        try:
            request = ServeTTSRequest.model_validate(payload)
            validate_tts_request(request)

        except (ValidationError, ValueError) as exc:
            await websocket.send_json(
                {
                    "type": "error",
                    "request_id": request_id,
                    "message": str(exc),
                }
            )
            await websocket.close(code=1008)
            return

        request = request.model_copy(
            update={
                "streaming": True,
                "format": "wav",
            }
        )

        sample_rate = get_sample_rate(get_engine())

        await websocket.send_json(
            {
                "type": "accepted",
                "request_id": request_id,
                "device": DEVICE,
                "format": "wav",
                "sample_rate": sample_rate,
            }
        )

        async for chunk in generate_streaming_chunks_async(request):
            if first_audio_at is None:
                first_audio_at = time.perf_counter()

                await websocket.send_json(
                    {
                        "type": "ttfa",
                        "request_id": request_id,
                        "ttfa_ms": round(
                            (first_audio_at - started_at) * 1000,
                            2,
                        ),
                    }
                )

            await websocket.send_bytes(chunk)

            chunks_sent += 1
            bytes_sent += len(chunk)

        total_ms = (time.perf_counter() - started_at) * 1000

        await websocket.send_json(
            {
                "type": "done",
                "request_id": request_id,
                "elapsed_ms": round(total_ms, 2),
                "chunks": chunks_sent,
                "bytes": bytes_sent,
            }
        )

        await websocket.close(code=1000)

    except WebSocketDisconnect:
        logger.warning(
            f"WebSocket client disconnected: request_id={request_id}"
        )

    except Exception as exc:
        logger.exception(
            f"WebSocket generation failed: request_id={request_id}: {exc}"
        )

        try:
            await websocket.send_json(
                {
                    "type": "error",
                    "request_id": request_id,
                    "message": str(exc),
                }
            )
            await websocket.close(code=1011)

        except Exception:
            pass
