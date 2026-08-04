from __future__ import annotations

import asyncio
import io
import os
import queue
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

PCM_SCALE = 32767.0


class ServerState:
    model_manager: ModelManager | None = None
    ready: bool = False
    startup_error: str | None = None
    model_load_ms: float | None = None


state = ServerState()

# Fish Speech uses shared inference buffers.
# Keep one inference request active at a time.
inference_lock = threading.Lock()


def validate_environment() -> None:
    if DEVICE != "cpu":
        raise RuntimeError(
            f"This image is configured for CPU inference, "
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

    if hasattr(decoder, "sample_rate"):
        return int(decoder.sample_rate)

    return 44100


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
        raise ValueError("Streaming supports WAV format only.")


def float_audio_to_pcm16(audio: np.ndarray) -> bytes:
    audio_array = np.asarray(audio, dtype=np.float32)
    audio_array = np.nan_to_num(audio_array)
    audio_array = np.clip(audio_array, -1.0, 1.0)

    pcm = (audio_array * PCM_SCALE).astype("<i2")
    return pcm.tobytes()


def encode_complete_audio(
    audio: np.ndarray,
    sample_rate: int,
    audio_format: str,
) -> bytes:
    audio_format = audio_format.lower()
    audio_array = np.asarray(audio, dtype=np.float32)
    audio_array = np.nan_to_num(audio_array)
    audio_array = np.clip(audio_array, -1.0, 1.0)

    if audio_format == "pcm":
        return float_audio_to_pcm16(audio_array)

    if audio_format != "wav":
        raise ValueError(
            "This server currently supports WAV and PCM output."
        )

    buffer = io.BytesIO()

    sf.write(
        buffer,
        audio_array,
        sample_rate,
        format="WAV",
        subtype="PCM_16",
    )

    return buffer.getvalue()


def content_type_for(audio_format: str) -> str:
    if audio_format == "wav":
        return "audio/wav"

    if audio_format == "pcm":
        return "application/octet-stream"

    return "application/octet-stream"


def generate_complete_audio(
    request: ServeTTSRequest,
) -> tuple[bytes, int, dict[str, float]]:
    engine = get_engine()

    inference_started_at = time.perf_counter()
    first_result_at: float | None = None
    final_audio: np.ndarray | None = None
    sample_rate = get_sample_rate(engine)

    with inference_lock:
        for result in engine.inference(request):
            if first_result_at is None:
                first_result_at = time.perf_counter()

            if result.code == "error":
                raise RuntimeError(str(result.error))

            if result.code == "final" and result.audio is not None:
                sample_rate, final_audio = result.audio

    inference_finished_at = time.perf_counter()

    if final_audio is None or final_audio.size == 0:
        raise RuntimeError("Fish Speech generated no audio.")

    encoding_started_at = time.perf_counter()

    audio_bytes = encode_complete_audio(
        final_audio,
        int(sample_rate),
        request.format,
    )

    encoding_finished_at = time.perf_counter()

    metrics = {
        "inference_ttfa_ms": round(
            (
                (first_result_at or inference_finished_at)
                - inference_started_at
            )
            * 1000,
            2,
        ),
        "inference_latency_ms": round(
            (inference_finished_at - inference_started_at) * 1000,
            2,
        ),
        "encoding_latency_ms": round(
            (encoding_finished_at - encoding_started_at) * 1000,
            2,
        ),
    }

    return audio_bytes, int(sample_rate), metrics


def generate_streaming_chunks(
    request: ServeTTSRequest,
) -> Iterator[bytes]:
    """
    Yield the streaming WAV header followed by PCM16 audio chunks.

    Fish Speech may emit a final concatenated waveform after all segments.
    That final waveform is intentionally not sent again.
    """
    engine = get_engine()

    header_sent = False
    segment_sent = False

    with inference_lock:
        for result in engine.inference(request):
            if result.code == "error":
                raise RuntimeError(str(result.error))

            if result.code == "header":
                if result.audio is None:
                    continue

                _, header = result.audio

                if isinstance(header, np.ndarray):
                    header_bytes = header.tobytes()
                else:
                    header_bytes = bytes(header)

                if header_bytes:
                    header_sent = True
                    yield header_bytes

            elif result.code == "segment":
                if result.audio is None:
                    continue

                _, audio = result.audio
                pcm_bytes = float_audio_to_pcm16(audio)

                if pcm_bytes:
                    segment_sent = True
                    yield pcm_bytes

            elif result.code == "final":
                # Streaming segments have already been returned.
                break

    if not header_sent:
        raise RuntimeError("Fish Speech did not generate a WAV header.")

    if not segment_sent:
        raise RuntimeError("Fish Speech generated no streaming audio.")


async def generate_streaming_chunks_async(
    request: ServeTTSRequest,
) -> AsyncIterator[bytes]:
    """
    Bridge the blocking Fish Speech generator into FastAPI asynchronously.
    """
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

    producer_thread = threading.Thread(
        target=producer,
        name=f"fish-tts-{uuid.uuid4().hex[:8]}",
        daemon=True,
    )
    producer_thread.start()

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

    model_load_started_at = time.perf_counter()

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

        state.model_load_ms = round(
            (time.perf_counter() - model_load_started_at) * 1000,
            2,
        )

        state.ready = True
        state.startup_error = None

        logger.info(
            f"Fish Speech loaded successfully on CPU in "
            f"{state.model_load_ms:.2f} ms"
        )

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
        "model_load_ms": state.model_load_ms,
        "http_tts": "/v1/tts",
        "websocket_tts": "/ws/tts",
        "port": 8000,
        "startup_error": state.startup_error,
    }

    return JSONResponse(
        content=response,
        status_code=200 if state.ready else 503,
    )


@app.post("/v1/tts")
async def http_tts(request: ServeTTSRequest):
    request_started_at = time.perf_counter()

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

        audio_bytes, sample_rate, inference_metrics = (
            await asyncio.to_thread(
                generate_complete_audio,
                request,
            )
        )

        total_latency_ms = round(
            (time.perf_counter() - request_started_at) * 1000,
            2,
        )

        extension = "wav" if request.format == "wav" else "pcm"

        return Response(
            content=audio_bytes,
            media_type=content_type_for(request.format),
            headers={
                "Content-Disposition": (
                    f'attachment; filename="speech.{extension}"'
                ),
                "X-Audio-Sample-Rate": str(sample_rate),
                "X-Total-Latency-Ms": str(total_latency_ms),
                "X-Inference-TTFA-Ms": str(
                    inference_metrics["inference_ttfa_ms"]
                ),
                "X-Inference-Latency-Ms": str(
                    inference_metrics["inference_latency_ms"]
                ),
                "X-Encoding-Latency-Ms": str(
                    inference_metrics["encoding_latency_ms"]
                ),
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
    connection_accepted_at = time.perf_counter()

    await websocket.accept()

    request_id = str(uuid.uuid4())

    request_received_at: float | None = None
    inference_started_at: float | None = None
    first_audio_at: float | None = None
    generation_finished_at: float | None = None

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
        request_received_at = time.perf_counter()

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

        inference_started_at = time.perf_counter()

        async for chunk in generate_streaming_chunks_async(request):
            now = time.perf_counter()

            if first_audio_at is None:
                first_audio_at = now

                server_ttfa_ms = (
                    first_audio_at - request_received_at
                ) * 1000

                inference_ttfa_ms = (
                    first_audio_at - inference_started_at
                ) * 1000

                await websocket.send_json(
                    {
                        "type": "ttfa",
                        "request_id": request_id,
                        "server_ttfa_ms": round(server_ttfa_ms, 2),
                        "inference_ttfa_ms": round(
                            inference_ttfa_ms,
                            2,
                        ),
                    }
                )

            await websocket.send_bytes(chunk)

            chunks_sent += 1
            bytes_sent += len(chunk)

        generation_finished_at = time.perf_counter()

        server_total_latency_ms = (
            generation_finished_at - request_received_at
        ) * 1000

        inference_latency_ms = (
            generation_finished_at - inference_started_at
        ) * 1000

        connection_to_done_ms = (
            generation_finished_at - connection_accepted_at
        ) * 1000

        await websocket.send_json(
            {
                "type": "done",
                "request_id": request_id,
                "server_ttfa_ms": (
                    round(
                        (first_audio_at - request_received_at) * 1000,
                        2,
                    )
                    if first_audio_at is not None
                    else None
                ),
                "inference_ttfa_ms": (
                    round(
                        (first_audio_at - inference_started_at) * 1000,
                        2,
                    )
                    if first_audio_at is not None
                    else None
                ),
                "server_total_latency_ms": round(
                    server_total_latency_ms,
                    2,
                ),
                "inference_latency_ms": round(
                    inference_latency_ms,
                    2,
                ),
                "connection_to_done_ms": round(
                    connection_to_done_ms,
                    2,
                ),
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
            f"WebSocket generation failed: "
            f"request_id={request_id}: {exc}"
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
