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
    """
    Update streamed WAV RIFF and data lengths after the transfer completes.
    """
    file_size = path.stat().st_size

    if file_size < 44:
        raise RuntimeError(
            f"Output is too small to be a WAV file: {file_size} bytes"
        )

    with path.open("r+b") as file:
        header = file.read(12)

        if header[:4] != b"RIFF":
            raise RuntimeError("Output does not begin with a RIFF header.")

        if header[8:12] != b"WAVE":
            raise RuntimeError("Output does not contain a WAVE signature.")

        file.seek(4)
        file.write(struct.pack("<I", file_size - 8))

        file.seek(0)
        content = file.read()

        data_offset = content.find(b"data")

        if data_offset < 0:
            raise RuntimeError("WAV data chunk was not found.")

        data_size_offset = data_offset + 4
        audio_data_offset = data_offset + 8
        audio_data_size = file_size - audio_data_offset

        file.seek(data_size_offset)
        file.write(struct.pack("<I", audio_data_size))


def play_audio(path: Path) -> None:
    if sys.platform.startswith("win"):
        try:
            os.startfile(str(path))  # type: ignore[attr-defined]
        except OSError as exc:
            print(f"[playback-error] {exc}")
            print(f"Open manually: {path}")
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

    print(f"No supported audio player found. Open manually: {path}")


def print_metric(
    label: str,
    value: float | int | None,
) -> None:
    if value is None:
        print(f"{label:<28}: N/A")
        return

    print(f"{label:<28}: {float(value):.2f} ms")


async def run_client(args: argparse.Namespace) -> None:
    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "text": args.text,
        "chunk_length": args.chunk_length,
        "format": "wav",
        "latency": args.latency,
        "reference_id": args.reference_id,
        "seed": args.seed,
        "use_memory_cache": args.memory_cache,
        "normalize": not args.no_normalize,
        "streaming": True,
        "max_new_tokens": args.max_new_tokens,
        "top_p": args.top_p,
        "repetition_penalty": args.repetition_penalty,
        "temperature": args.temperature,
    }

    process_started_at = time.perf_counter()
    connected_at: float | None = None
    request_sent_at: float | None = None
    first_audio_at: float | None = None
    done_received_at: float | None = None
    connection_closed_at: float | None = None

    bytes_received = 0
    chunks_received = 0
    completed = False

    server_ttfa_ms: float | None = None
    inference_ttfa_ms: float | None = None
    server_total_latency_ms: float | None = None
    inference_latency_ms: float | None = None
    connection_to_done_ms: float | None = None

    print(f"[connect] {args.url}")

    try:
        async with websockets.connect(
            args.url,
            open_timeout=args.connect_timeout,
            ping_interval=20,
            ping_timeout=None,
            close_timeout=10,
            max_size=None,
        ) as websocket:
            connected_at = time.perf_counter()

            connection_latency_ms = (
                connected_at - process_started_at
            ) * 1000

            print(
                f"[connection-latency] "
                f"{connection_latency_ms:.2f} ms"
            )

            await websocket.send(json.dumps(payload))
            request_sent_at = time.perf_counter()

            with output.open("wb") as output_file:
                async for message in websocket:
                    if isinstance(message, bytes):
                        now = time.perf_counter()

                        if first_audio_at is None:
                            first_audio_at = now

                            client_ttfa_ms = (
                                first_audio_at - request_sent_at
                            ) * 1000

                            end_to_end_ttfa_ms = (
                                first_audio_at - process_started_at
                            ) * 1000

                            print(
                                f"[client-ttfa] "
                                f"{client_ttfa_ms:.2f} ms"
                            )

                            print(
                                f"[end-to-end-ttfa] "
                                f"{end_to_end_ttfa_ms:.2f} ms"
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

                    if event_type == "ttfa":
                        server_ttfa_ms = event.get(
                            "server_ttfa_ms"
                        )
                        inference_ttfa_ms = event.get(
                            "inference_ttfa_ms"
                        )

                    elif event_type == "done":
                        done_received_at = time.perf_counter()
                        completed = True

                        server_ttfa_ms = event.get(
                            "server_ttfa_ms",
                            server_ttfa_ms,
                        )

                        inference_ttfa_ms = event.get(
                            "inference_ttfa_ms",
                            inference_ttfa_ms,
                        )

                        server_total_latency_ms = event.get(
                            "server_total_latency_ms"
                        )

                        inference_latency_ms = event.get(
                            "inference_latency_ms"
                        )

                        connection_to_done_ms = event.get(
                            "connection_to_done_ms"
                        )

                    elif event_type == "error":
                        raise RuntimeError(
                            event.get(
                                "message",
                                "Unknown server error",
                            )
                        )

            connection_closed_at = time.perf_counter()

    except Exception:
        if output.exists() and output.stat().st_size == 0:
            output.unlink()

        raise

    if not completed:
        raise RuntimeError(
            "The WebSocket closed before the done event was received."
        )

    if request_sent_at is None:
        raise RuntimeError("Request timing was not initialized.")

    if done_received_at is None:
        done_received_at = time.perf_counter()

    if connection_closed_at is None:
        connection_closed_at = done_received_at

    finalize_wav(output)

    connection_latency_ms = (
        (connected_at - process_started_at) * 1000
        if connected_at is not None
        else None
    )

    client_ttfa_ms = (
        (first_audio_at - request_sent_at) * 1000
        if first_audio_at is not None
        else None
    )

    end_to_end_ttfa_ms = (
        (first_audio_at - process_started_at) * 1000
        if first_audio_at is not None
        else None
    )

    client_total_latency_ms = (
        done_received_at - request_sent_at
    ) * 1000

    end_to_end_latency_ms = (
        done_received_at - process_started_at
    ) * 1000

    websocket_close_latency_ms = (
        connection_closed_at - done_received_at
    ) * 1000

    print()
    print("=" * 58)
    print("LATENCY SUMMARY")
    print("=" * 58)

    print_metric(
        "Connection latency",
        connection_latency_ms,
    )

    print_metric(
        "Client TTFA",
        client_ttfa_ms,
    )

    print_metric(
        "End-to-end TTFA",
        end_to_end_ttfa_ms,
    )

    print_metric(
        "Server TTFA",
        server_ttfa_ms,
    )

    print_metric(
        "Inference TTFA",
        inference_ttfa_ms,
    )

    print_metric(
        "Client total latency",
        client_total_latency_ms,
    )

    print_metric(
        "End-to-end latency",
        end_to_end_latency_ms,
    )

    print_metric(
        "Server total latency",
        server_total_latency_ms,
    )

    print_metric(
        "Inference latency",
        inference_latency_ms,
    )

    print_metric(
        "Server connection-to-done",
        connection_to_done_ms,
    )

    print_metric(
        "WebSocket close latency",
        websocket_close_latency_ms,
    )

    print("=" * 58)
    print(f"Output file                 : {output}")
    print(f"Audio bytes received        : {bytes_received:,}")
    print(f"Binary chunks received      : {chunks_received}")
    print("=" * 58)

    if args.play:
        play_audio(output)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fish Speech WebSocket latency test client"
    )

    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"WebSocket URL. Default: {DEFAULT_URL}",
    )

    parser.add_argument(
        "--text",
        default=None,
        help="Text to synthesize",
    )

    parser.add_argument(
        "--output",
        default="fish-output.wav",
        help="Output WAV file",
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
