from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import struct
import subprocess
import sys
import time
from pathlib import Path

import websockets


DEFAULT_URL = "ws://127.0.0.1:8000/ws/tts"


def finalize_wav(path: Path) -> None:
    file_size = path.stat().st_size

    if file_size < 44:
        raise RuntimeError(
            f"Output is too small to be a WAV file: {file_size} bytes"
        )

    with path.open("r+b") as file:
        header = file.read(12)

        if header[:4] != b"RIFF" or header[8:12] != b"WAVE":
            raise RuntimeError("The server response is not a valid WAV file.")

        file.seek(4)
        file.write(struct.pack("<I", file_size - 8))

        file.seek(0)
        content = file.read()

        data_offset = content.find(b"data")

        if data_offset < 0:
            raise RuntimeError("WAV data section was not found.")

        audio_start = data_offset + 8
        audio_size = file_size - audio_start

        file.seek(data_offset + 4)
        file.write(struct.pack("<I", audio_size))


def play_audio(path: Path) -> None:
    if sys.platform.startswith("win"):
        os.startfile(path)  # type: ignore[attr-defined]
        return

    players = [
        ["ffplay", "-autoexit", "-nodisp", str(path)],
        ["afplay", str(path)],
        ["aplay", str(path)],
    ]

    for command in players:
        if shutil.which(command[0]):
            subprocess.run(command, check=False)
            return

    print(f"No audio player found. Open manually: {path}")


async def run_client(args: argparse.Namespace) -> None:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "text": args.text,
        "chunk_length": args.chunk_length,
        "format": "wav",
        "latency": "normal",
        "reference_id": None,
        "seed": args.seed,
        "use_memory_cache": "off",
        "normalize": True,
        "streaming": True,
        "max_new_tokens": args.max_new_tokens,
        "top_p": args.top_p,
        "repetition_penalty": args.repetition_penalty,
        "temperature": args.temperature,
    }

    started_at = time.perf_counter()
    first_audio_at: float | None = None

    bytes_received = 0
    chunks_received = 0
    completed = False

    print(f"[connect] {args.url}")

    async with websockets.connect(
        args.url,
        open_timeout=args.connect_timeout,
        ping_interval=20,
        ping_timeout=None,
        close_timeout=10,
        max_size=None,
    ) as websocket:
        await websocket.send(json.dumps(payload))

        with output.open("wb") as output_file:
            async for message in websocket:
                if isinstance(message, bytes):
                    if first_audio_at is None:
                        first_audio_at = time.perf_counter()

                        print(
                            "[client-ttfa] "
                            f"{(first_audio_at - started_at) * 1000:.2f} ms"
                        )

                    output_file.write(message)
                    output_file.flush()

                    bytes_received += len(message)
                    chunks_received += 1
                    continue

                event = json.loads(message)
                event_type = event.get("type", "unknown")

                print(
                    f"[{event_type}] "
                    f"{json.dumps(event, ensure_ascii=False)}"
                )

                if event_type == "error":
                    raise RuntimeError(
                        event.get("message", "Unknown server error")
                    )

                if event_type == "done":
                    completed = True

    if not completed:
        raise RuntimeError(
            "The WebSocket closed before the done event was received."
        )

    finalize_wav(output)

    elapsed = time.perf_counter() - started_at

    print(f"[saved] {output}")
    print(f"[bytes] {bytes_received:,}")
    print(f"[chunks] {chunks_received}")
    print(f"[elapsed] {elapsed:.2f} seconds")

    if args.play:
        play_audio(output)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fish Speech WebSocket test client"
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
        "--seed",
        type=int,
        default=None,
    )

    parser.add_argument(
        "--connect-timeout",
        type=float,
        default=60,
    )

    parser.add_argument(
        "--play",
        action="store_true",
    )

    args = parser.parse_args()

    if not args.text:
        args.text = input("Text: ").strip()

    if not args.text:
        parser.error("Text cannot be empty.")

    return args


def main() -> None:
    arguments = parse_arguments()

    try:
        asyncio.run(run_client(arguments))

    except KeyboardInterrupt:
        print("\nCancelled.")
        raise SystemExit(130)

    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
