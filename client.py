from __future__ import annotations

import argparse
import asyncio
import json
import shutil
import struct
import subprocess
import time
from pathlib import Path

import websockets


def finalize_wav(path: Path) -> None:
    data = bytearray(path.read_bytes())
    if len(data) < 44 or data[:4] != b"RIFF" or data[8:12] != b"WAVE":
        return
    struct.pack_into("<I", data, 4, len(data) - 8)
    marker = data.find(b"data")
    if marker >= 0 and marker + 8 <= len(data):
        struct.pack_into("<I", data, marker + 4, len(data) - marker - 8)
    path.write_bytes(data)


def play(path: Path) -> None:
    for command in (["ffplay", "-nodisp", "-autoexit", str(path)], ["afplay", str(path)], ["aplay", str(path)]):
        if shutil.which(command[0]):
            subprocess.run(command, check=False)
            return
    print("[playback] Install ffplay, afplay, or aplay to use --play")


async def run(args: argparse.Namespace) -> None:
    payload = {
        "text": args.text,
        "reference_id": args.reference_id,
        "chunk_length": args.chunk_length,
        "format": "wav",
        "latency": args.latency,
        "seed": args.seed,
        "use_memory_cache": args.memory_cache,
        "normalize": not args.no_normalize,
        "streaming": True,
        "max_new_tokens": args.max_new_tokens,
        "top_p": args.top_p,
        "repetition_penalty": args.repetition_penalty,
        "temperature": args.temperature,
    }

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    first_audio = None

    print(f"[connect] {args.url}")
    async with websockets.connect(args.url, max_size=None, ping_timeout=120) as ws:
        await ws.send(json.dumps(payload))
        with output.open("wb") as file:
            async for message in ws:
                if isinstance(message, bytes):
                    if first_audio is None:
                        first_audio = time.perf_counter()
                    file.write(message)
                    continue

                event = json.loads(message)
                print(f"[{event.get('type', 'event')}] {event}")
                if event.get("type") == "error":
                    raise RuntimeError(event.get("message", "Unknown server error"))
                if event.get("type") == "done":
                    break

    finalize_wav(output)
    print(f"[saved] {output}")
    print(f"[size] {output.stat().st_size:,} bytes")
    print(f"[elapsed] {time.perf_counter() - started:.3f}s")
    if first_audio is not None:
        print(f"[client-ttfa] {(first_audio - started) * 1000:.2f}ms")
    if args.play:
        play(output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fish Speech S2 Pro WebSocket client")
    parser.add_argument("--url", default="ws://127.0.0.1:8000/ws/tts")
    parser.add_argument("--text")
    parser.add_argument("--output", default="output.wav")
    parser.add_argument("--reference-id", default=None)
    parser.add_argument("--chunk-length", type=int, default=200)
    parser.add_argument("--latency", choices=["normal", "balanced"], default="normal")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--memory-cache", choices=["on", "off"], default="off")
    parser.add_argument("--no-normalize", action="store_true")
    parser.add_argument("--max-new-tokens", type=int, default=1024)
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--repetition-penalty", type=float, default=1.1)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--play", action="store_true")
    args = parser.parse_args()
    if not args.text:
        args.text = input("Text: ").strip()
    if not args.text:
        parser.error("text must not be empty")
    return args


if __name__ == "__main__":
    asyncio.run(run(parse_args()))
