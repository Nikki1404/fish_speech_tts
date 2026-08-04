from __future__ import annotations

import asyncio
import io
import os
import threading
import time
import uuid
from contextlib import asynccontextmanager
from typing import Any

import numpy as np
import soundfile as sf
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, Response
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
WS_CHUNK_SIZE = int(os.getenv("WS_CHUNK_SIZE", str(64 * 1024)))


class ServerState:
    model_manager: ModelManager | None = None
    ready = False
    startup_error: str | None = None
    model_load_ms: float | None = None


state = ServerState()
inference_lock = threading.Lock()


def validate_environment() -> None:
    if DEVICE != "cpu":
        raise RuntimeError(
            f"This build is CPU-only, but DEVICE={DEVICE!r}"
        )


def get_engine() -> Any:
    if not state.ready or state.model_manager is None:
        raise RuntimeError(
            state.startup_error or "Fish Speech model is not ready."
        )

    return state.model_manager.tts_inference_engine


def validate_request(request: ServeTTSRequest) -> None:
    text = request.text.strip()

    if not text:
        raise ValueError("Text cannot be empty.")

    if MAX_TEXT_LENGTH > 0 and len(text) > MAX_TEXT_LENGTH:
        raise ValueError(
            f"Text exceeds {MAX_TEXT_LENGTH} characters."
        )


def normalize_audio(audio: np.ndarray) -> np.ndarray:
    output = np.asarray(audio, dtype=np.float32)
    output = np.squeeze(output)
    output = np.nan_to_num(output, nan=0.0, posinf=1.0, neginf=-1.0)
    output = np.clip(output, -1.0, 1.0)

    if output.ndim != 1:
        raise RuntimeError(
            f"Expected mono audio, received shape {output.shape}."
        )

    return output


def create_valid_wav(
    audio: np.ndarray,
    sample_rate: int,
) -> bytes:
    audio = normalize_audio(audio)

    buffer = io.BytesIO()

    sf.write(
        buffer,
        audio,
        int(sample_rate),
        format="WAV",
        subtype="PCM_16",
    )

    wav_bytes = buffer.getvalue()

    if len(wav_bytes) < 44:
        raise RuntimeError("Generated WAV output is unexpectedly small.")

    if wav_bytes[:4] != b"RIFF" or wav_bytes[8:12] != b"WAVE":
        raise RuntimeError("Generated data is not a valid WAV file.")

    return wav_bytes


def generate_wav(
    request: ServeTTSRequest,
) -> tuple[bytes, dict[str, float | int]]:
    """
    Generate complete audio and encode it as a valid PCM16 WAV.

    A non-streaming request is deliberately used internally so the resulting
    audio is encoded from one final waveform instead of manually joining
    internal streaming segments.
    """
    engine = get_engine()

    inference_request = request.model_copy(
        update={
            "streaming": False,
            "format": "wav",
        }
    )

    inference_started_at = time.perf_counter()
    first_result_at: float | None = None
    final_audio: np.ndarray | None = None
    sample_rate: int | None = None

    with inference_lock:
        for result in engine.inference(inference_request):
            now = time.perf_counter()

            if first_result_at is None:
                first_result_at = now

            if result.code == "error":
                raise RuntimeError(str(result.error))

            if result.code == "final" and result.audio is not None:
                result_sample_rate, result_audio = result.audio
                sample_rate = int(result_sample_rate)
                final_audio = np.asarray(result_audio)

    inference_finished_at = time.perf_counter()

    if final_audio is None or final_audio.size == 0:
        raise RuntimeError("Fish Speech returned no final audio.")

    if sample_rate is None:
        raise RuntimeError("Fish Speech returned no sample rate.")

    encoding_started_at = time.perf_counter()
    wav_bytes = create_valid_wav(final_audio, sample_rate)
    encoding_finished_at = time.perf_counter()

    metrics: dict[str, float | int] = {
        "sample_rate": sample_rate,
        "inference_first_result_ms": round(
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
        "wav_encoding_latency_ms": round(
            (encoding_finished_at - encoding_started_at) * 1000,
            2,
        ),
        "audio_bytes": len(wav_bytes),
    }

    return wav_bytes, metrics


@asynccontextmanager
async def lifespan(_: FastAPI):
    validate_environment()

    load_started_at = time.perf_counter()

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
            (time.perf_counter() - load_started_at) * 1000,
            2,
        )
        state.ready = True
        state.startup_error = None

        logger.info(
            f"Fish Speech loaded in {state.model_load_ms:.2f} ms"
        )

    except Exception as exc:
        state.ready = False
        state.startup_error = str(exc)
        logger.exception(f"Model startup failed: {exc}")
        raise

    yield

    state.ready = False


app = FastAPI(
    title="Fish Speech CPU TTS",
    version="1.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root() -> dict[str, Any]:
    return {
        "service": "Fish Speech CPU TTS",
        "device": DEVICE,
        "http_tts": "/v1/tts",
        "websocket_tts": "/ws/tts",
        "health": "/health",
    }


@app.get("/health")
async def health() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok" if state.ready else "loading",
            "ready": state.ready,
            "device": DEVICE,
            "model": "fishaudio/s2-pro",
            "model_load_ms": state.model_load_ms,
            "startup_error": state.startup_error,
        },
        status_code=200 if state.ready else 503,
    )


@app.post("/v1/tts")
async def http_tts(request: ServeTTSRequest) -> Response:
    request_started_at = time.perf_counter()

    try:
        validate_request(request)

        if not state.ready:
            raise HTTPException(
                status_code=503,
                detail=state.startup_error or "Model is loading.",
            )

        wav_bytes, metrics = await asyncio.to_thread(
            generate_wav,
            request,
        )

        total_latency_ms = round(
            (time.perf_counter() - request_started_at) * 1000,
            2,
        )

        return Response(
            content=wav_bytes,
            media_type="audio/wav",
            headers={
                "Content-Disposition": (
                    'attachment; filename="fish-speech.wav"'
                ),
                "X-Total-Latency-Ms": str(total_latency_ms),
                "X-Inference-Latency-Ms": str(
                    metrics["inference_latency_ms"]
                ),
                "X-Wav-Encoding-Latency-Ms": str(
                    metrics["wav_encoding_latency_ms"]
                ),
                "X-Audio-Sample-Rate": str(metrics["sample_rate"]),
                "X-Audio-Bytes": str(metrics["audio_bytes"]),
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
    connection_started_at = time.perf_counter()
    await websocket.accept()

    request_id = str(uuid.uuid4())
    request_received_at: float | None = None
    generation_started_at: float | None = None
    first_binary_sent_at: float | None = None

    try:
        if not state.ready:
            await websocket.send_json(
                {
                    "type": "error",
                    "request_id": request_id,
                    "message": (
                        state.startup_error or "Model is loading."
                    ),
                }
            )
            await websocket.close(code=1013)
            return

        payload = await websocket.receive_json()
        request_received_at = time.perf_counter()

        try:
            request = ServeTTSRequest.model_validate(payload)
            validate_request(request)

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

        await websocket.send_json(
            {
                "type": "accepted",
                "request_id": request_id,
                "device": DEVICE,
                "audio_format": "wav",
                "delivery": "complete-wav-chunked",
            }
        )

        generation_started_at = time.perf_counter()

        wav_bytes, metrics = await asyncio.to_thread(
            generate_wav,
            request,
        )

        generation_finished_at = time.perf_counter()

        chunk_count = 0
        sent_bytes = 0

        for offset in range(0, len(wav_bytes), WS_CHUNK_SIZE):
            chunk = wav_bytes[offset : offset + WS_CHUNK_SIZE]

            if first_binary_sent_at is None:
                first_binary_sent_at = time.perf_counter()

                await websocket.send_json(
                    {
                        "type": "ttfa",
                        "request_id": request_id,
                        "server_ttfa_ms": round(
                            (
                                first_binary_sent_at
                                - request_received_at
                            )
                            * 1000,
                            2,
                        ),
                        "generation_latency_ms": round(
                            (
                                generation_finished_at
                                - generation_started_at
                            )
                            * 1000,
                            2,
                        ),
                        "inference_latency_ms": metrics[
                            "inference_latency_ms"
                        ],
                    }
                )

            await websocket.send_bytes(chunk)
            chunk_count += 1
            sent_bytes += len(chunk)

        finished_at = time.perf_counter()

        await websocket.send_json(
            {
                "type": "done",
                "request_id": request_id,
                "server_ttfa_ms": (
                    round(
                        (
                            first_binary_sent_at
                            - request_received_at
                        )
                        * 1000,
                        2,
                    )
                    if first_binary_sent_at is not None
                    else None
                ),
                "inference_first_result_ms": metrics[
                    "inference_first_result_ms"
                ],
                "inference_latency_ms": metrics[
                    "inference_latency_ms"
                ],
                "wav_encoding_latency_ms": metrics[
                    "wav_encoding_latency_ms"
                ],
                "generation_latency_ms": round(
                    (
                        generation_finished_at
                        - generation_started_at
                    )
                    * 1000,
                    2,
                ),
                "server_total_latency_ms": round(
                    (finished_at - request_received_at) * 1000,
                    2,
                ),
                "connection_to_done_ms": round(
                    (finished_at - connection_started_at) * 1000,
                    2,
                ),
                "sample_rate": metrics["sample_rate"],
                "chunks": chunk_count,
                "bytes": sent_bytes,
            }
        )

        await websocket.close(code=1000)

    except WebSocketDisconnect:
        logger.warning(
            f"Client disconnected: request_id={request_id}"
        )

    except Exception as exc:
        logger.exception(
            f"WebSocket TTS failed: request_id={request_id}: {exc}"
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



#client.py

from __future__ import annotations

import argparse
import asyncio
import json
import os
import struct
import sys
import time
import wave
from pathlib import Path
from typing import Any

import sounddevice as sd
import websockets


DEFAULT_URL = os.getenv(
    "FISH_WS_URL",
    "ws://127.0.0.1:8000/ws/tts",
)


def validate_wav(path: Path) -> dict[str, int]:
    if not path.exists():
        raise RuntimeError(f"Output file does not exist: {path}")

    size = path.stat().st_size

    if size < 44:
        raise RuntimeError(
            f"Output is too small to be WAV audio: {size} bytes"
        )

    with path.open("rb") as file:
        header = file.read(12)

    if header[:4] != b"RIFF" or header[8:12] != b"WAVE":
        raise RuntimeError(
            f"Invalid WAV signature: {header!r}"
        )

    try:
        with wave.open(str(path), "rb") as wav:
            return {
                "channels": wav.getnchannels(),
                "sample_width": wav.getsampwidth(),
                "sample_rate": wav.getframerate(),
                "frames": wav.getnframes(),
            }

    except wave.Error as exc:
        raise RuntimeError(
            f"Saved file is not a readable WAV: {exc}"
        ) from exc


def play_wav(path: Path) -> None:
    """
    Read the saved WAV and play its PCM data using sounddevice.
    """
    info = validate_wav(path)

    if info["sample_width"] != 2:
        raise RuntimeError(
            f"Expected PCM16 WAV, got sample width "
            f"{info['sample_width']} bytes."
        )

    with wave.open(str(path), "rb") as wav:
        pcm = wav.readframes(wav.getnframes())

    if not pcm:
        raise RuntimeError("WAV file contains no PCM audio.")

    print(
        f"[playback] sample_rate={info['sample_rate']}, "
        f"channels={info['channels']}, "
        f"frames={info['frames']}"
    )

    stream = sd.RawOutputStream(
        samplerate=info["sample_rate"],
        channels=info["channels"],
        dtype="int16",
        latency="low",
    )

    try:
        stream.start()
        stream.write(pcm)
        stream.stop()
    finally:
        stream.close()


def print_metric(
    label: str,
    value: float | int | None,
) -> None:
    if value is None:
        print(f"{label:<30}: N/A")
    else:
        print(f"{label:<30}: {float(value):.2f} ms")


async def run_client(args: argparse.Namespace) -> None:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "text": args.text,
        "chunk_length": args.chunk_length,
        "format": "wav",
        "latency": args.latency,
        "reference_id": args.reference_id,
        "seed": args.seed,
        "use_memory_cache": args.memory_cache,
        "normalize": not args.no_normalize,
        "streaming": False,
        "max_new_tokens": args.max_new_tokens,
        "top_p": args.top_p,
        "repetition_penalty": args.repetition_penalty,
        "temperature": args.temperature,
    }

    process_started_at = time.perf_counter()
    connected_at: float | None = None
    request_sent_at: float | None = None
    first_binary_at: float | None = None
    done_at: float | None = None

    bytes_received = 0
    chunks_received = 0
    completed = False
    server_metrics: dict[str, Any] = {}

    if output.exists():
        output.unlink()

    print(f"[connect] {args.url}")
    print(f"[output] {output}")

    try:
        async with websockets.connect(
            args.url,
            open_timeout=args.connect_timeout,
            ping_interval=20,
            ping_timeout=None,
            close_timeout=15,
            max_size=None,
        ) as websocket:
            connected_at = time.perf_counter()

            print(
                "[connection-latency] "
                f"{(connected_at - process_started_at) * 1000:.2f} ms"
            )

            await websocket.send(json.dumps(payload))
            request_sent_at = time.perf_counter()

            with output.open("wb") as file:
                async for message in websocket:
                    if isinstance(message, bytes):
                        if first_binary_at is None:
                            first_binary_at = time.perf_counter()

                            print(
                                "[client-ttfa] "
                                f"{(first_binary_at - request_sent_at) * 1000:.2f} ms"
                            )

                        file.write(message)
                        bytes_received += len(message)
                        chunks_received += 1
                        continue

                    event = json.loads(message)
                    event_type = event.get("type", "unknown")

                    print(
                        f"[{event_type}] "
                        f"{json.dumps(event, ensure_ascii=False)}"
                    )

                    if event_type == "ttfa":
                        server_metrics.update(event)

                    elif event_type == "done":
                        server_metrics.update(event)
                        done_at = time.perf_counter()
                        completed = True

                    elif event_type == "error":
                        raise RuntimeError(
                            event.get(
                                "message",
                                "Unknown server error",
                            )
                        )

    except Exception:
        if output.exists() and output.stat().st_size == 0:
            output.unlink()
        raise

    if not completed:
        raise RuntimeError(
            "WebSocket closed before receiving the done event."
        )

    if request_sent_at is None:
        raise RuntimeError("Request timing was not recorded.")

    if done_at is None:
        done_at = time.perf_counter()

    wav_info = validate_wav(output)

    client_ttfa_ms = (
        (first_binary_at - request_sent_at) * 1000
        if first_binary_at is not None
        else None
    )

    end_to_end_ttfa_ms = (
        (first_binary_at - process_started_at) * 1000
        if first_binary_at is not None
        else None
    )

    client_total_ms = (done_at - request_sent_at) * 1000
    end_to_end_ms = (done_at - process_started_at) * 1000

    print()
    print("=" * 60)
    print("LATENCY SUMMARY")
    print("=" * 60)

    print_metric(
        "Connection latency",
        (
            (connected_at - process_started_at) * 1000
            if connected_at is not None
            else None
        ),
    )
    print_metric("Client TTFA", client_ttfa_ms)
    print_metric("End-to-end TTFA", end_to_end_ttfa_ms)
    print_metric(
        "Server TTFA",
        server_metrics.get("server_ttfa_ms"),
    )
    print_metric(
        "Inference first result",
        server_metrics.get("inference_first_result_ms"),
    )
    print_metric(
        "Inference latency",
        server_metrics.get("inference_latency_ms"),
    )
    print_metric(
        "WAV encoding latency",
        server_metrics.get("wav_encoding_latency_ms"),
    )
    print_metric(
        "Generation latency",
        server_metrics.get("generation_latency_ms"),
    )
    print_metric("Client total latency", client_total_ms)
    print_metric("End-to-end latency", end_to_end_ms)
    print_metric(
        "Server total latency",
        server_metrics.get("server_total_latency_ms"),
    )

    print("=" * 60)
    print(f"Saved WAV                    : {output}")
    print(f"File size                    : {output.stat().st_size:,}")
    print(f"Received bytes               : {bytes_received:,}")
    print(f"Received chunks              : {chunks_received}")
    print(f"Sample rate                  : {wav_info['sample_rate']}")
    print(f"Channels                     : {wav_info['channels']}")
    print(f"Sample width                 : {wav_info['sample_width']}")
    print(f"Frames                       : {wav_info['frames']}")
    print("=" * 60)

    if args.play:
        await asyncio.to_thread(play_wav, output)
        print("[playback] completed")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fish Speech WAV WebSocket client"
    )

    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
    )
    parser.add_argument(
        "--text",
        default=None,
    )
    parser.add_argument(
        "--output",
        default="fish-output.wav",
    )
    parser.add_argument(
        "--chunk-length",
        type=int,
        default=200,
    )
    parser.add_argument(
        "--latency",
        choices=["normal", "balanced"],
        default="normal",
    )
    parser.add_argument(
        "--reference-id",
        default=None,
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--memory-cache",
        choices=["on", "off"],
        default="off",
    )
    parser.add_argument(
        "--no-normalize",
        action="store_true",
    )
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=256,
    )
    parser.add_argument(
        "--top-p",
        type=float,
        default=0.8,
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.8,
    )
    parser.add_argument(
        "--repetition-penalty",
        type=float,
        default=1.1,
    )
    parser.add_argument(
        "--connect-timeout",
        type=float,
        default=120,
    )

    playback = parser.add_mutually_exclusive_group()

    playback.add_argument(
        "--play",
        dest="play",
        action="store_true",
    )
    playback.add_argument(
        "--no-play",
        dest="play",
        action="store_false",
    )

    parser.set_defaults(play=True)

    args = parser.parse_args()

    if not args.text:
        args.text = input("Text: ").strip()

    if not args.text:
        parser.error("Text cannot be empty.")

    return args


def main() -> None:
    args = parse_arguments()

    try:
        asyncio.run(run_client(args))

    except KeyboardInterrupt:
        print("\nCancelled.")
        raise SystemExit(130)

    except sd.PortAudioError as exc:
        print(f"[audio-device-error] {exc}", file=sys.stderr)
        print(
            "Run the client on your Windows laptop, not the EC2 server.",
            file=sys.stderr,
        )
        raise SystemExit(1)

    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
