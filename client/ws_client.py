#!/usr/bin/env python3
import argparse
import asyncio
import json
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from websockets.asyncio.client import connect


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Test Fish Speech S2 Pro through the WebSocket gateway."
    )
    parser.add_argument("--url", default="ws://127.0.0.1:8880/ws/tts")
    parser.add_argument("--api-key", default="")
    parser.add_argument(
        "--text",
        default="[professional broadcast tone] Hello from Fish Audio S2 Pro.",
    )
    parser.add_argument("--reference-id", default=None)
    parser.add_argument("--output", default="output/fish_s2_pro.wav")
    parser.add_argument("--chunk-length", type=int, default=200)
    parser.add_argument("--latency", choices=["normal", "balanced"], default="normal")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--memory-cache", choices=["on", "off"], default="off")
    parser.add_argument("--no-normalize", action="store_true")
    parser.add_argument("--non-streaming", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=1024)
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--repetition-penalty", type=float, default=1.1)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--play", action="store_true")
    return parser.parse_args()



def finalize_streaming_wav(path: Path) -> bool:
    """Patch RIFF and data sizes after receiving an unknown-length WAV stream."""
    data = bytearray(path.read_bytes())
    if len(data) < 44 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return False

    data_offset = data.find(b"data", 12, min(len(data), 512))
    if data_offset < 0 or data_offset + 8 > len(data):
        return False

    struct.pack_into("<I", data, 4, len(data) - 8)
    struct.pack_into("<I", data, data_offset + 4, len(data) - (data_offset + 8))
    path.write_bytes(data)
    return True


def play_audio(path: Path) -> None:
    candidates = [
        ("ffplay", ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str(path)]),
        ("afplay", ["afplay", str(path)]),
        ("aplay", ["aplay", str(path)]),
    ]
    for executable, command in candidates:
        if shutil.which(executable):
            subprocess.run(command, check=False)
            return
    print("[play] No ffplay, afplay, or aplay command was found.")


def print_event(event: dict[str, Any]) -> None:
    event_type = event.get("type", "event")
    print(f"[{event_type}] {json.dumps(event, ensure_ascii=False)}")


async def run(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    request: dict[str, Any] = {
        "text": args.text,
        "reference_id": args.reference_id,
        "chunk_length": args.chunk_length,
        "format": "wav",
        "latency": args.latency,
        "seed": args.seed,
        "use_memory_cache": args.memory_cache,
        "normalize": not args.no_normalize,
        "streaming": not args.non_streaming,
        "max_new_tokens": args.max_new_tokens,
        "top_p": args.top_p,
        "repetition_penalty": args.repetition_penalty,
        "temperature": args.temperature,
    }
    request = {key: value for key, value in request.items() if value is not None}

    headers = {}
    if args.api_key:
        headers["Authorization"] = f"Bearer {args.api_key}"

    started = time.perf_counter()
    first_audio_at: float | None = None
    bytes_received = 0
    completed = False

    try:
        async with connect(
            args.url,
            additional_headers=headers,
            max_size=None,
            ping_interval=20,
            ping_timeout=60,
            close_timeout=10,
        ) as websocket:
            await websocket.send(json.dumps(request, ensure_ascii=False))

            with output.open("wb") as audio_file:
                async for message in websocket:
                    if isinstance(message, bytes):
                        if first_audio_at is None:
                            first_audio_at = time.perf_counter()
                        audio_file.write(message)
                        bytes_received += len(message)
                        continue

                    event = json.loads(message)
                    print_event(event)
                    if event.get("type") == "error":
                        return 1
                    if event.get("type") == "done":
                        completed = True

    except Exception as exc:
        print(f"[client-error] {exc}", file=sys.stderr)
        return 1

    elapsed = time.perf_counter() - started
    print(f"[saved] {output}")
    print(f"[bytes] {bytes_received}")
    print(f"[elapsed] {elapsed:.3f}s")
    if first_audio_at is not None:
        print(f"[client-ttfa] {(first_audio_at - started) * 1000:.2f}ms")

    if not args.non_streaming and bytes_received > 0 and finalize_streaming_wav(output):
        print("[wav-finalized] RIFF and data sizes updated")

    if not completed or bytes_received == 0:
        print("[error] The stream did not complete with audio.", file=sys.stderr)
        return 1

    if args.play:
        play_audio(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(run(parse_args())))
