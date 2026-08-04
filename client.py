from __future__ import annotations

import argparse
import asyncio
import json
import sys
import time
import wave
from pathlib import Path
from typing import Any

import sounddevice as sd
import websockets


DEFAULT_URL = "ws://127.0.0.1:8000/ws/tts"
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 1
SAMPLE_WIDTH_BYTES = 2  # int16


def extract_pcm(chunk: bytes) -> bytes:
    """
    Remove a WAV header when the incoming binary chunk starts with RIFF.

    Normal PCM chunks are returned unchanged.
    """
    if not chunk:
        return b""

    if not chunk.startswith(b"RIFF"):
        return chunk

    data_position = chunk.find(b"data")

    if data_position == -1:
        # Header-only chunk.
        return b""

    pcm_start = data_position + 8

    if pcm_start >= len(chunk):
        return b""

    return chunk[pcm_start:]


def align_pcm_frames(pcm: bytes, channels: int) -> bytes:
    """
    Remove trailing incomplete PCM frames.
    """
    frame_size = channels * SAMPLE_WIDTH_BYTES

    if frame_size <= 0:
        return b""

    usable = len(pcm) - (len(pcm) % frame_size)
    return pcm[:usable]


def print_metric(label: str, value: float | int | None) -> None:
    if value is None:
        print(f"{label:<28}: N/A")
    else:
        print(f"{label:<28}: {float(value):.2f} ms")


async def run_client(args: argparse.Namespace) -> None:
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
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

    client_started_at = time.perf_counter()
    connected_at: float | None = None
    request_sent_at: float | None = None
    first_pcm_at: float | None = None
    done_at: float | None = None

    sample_rate = DEFAULT_SAMPLE_RATE
    channels = DEFAULT_CHANNELS

    received_binary_bytes = 0
    saved_pcm_bytes = 0
    played_pcm_bytes = 0
    audio_chunks = 0
    completed = False

    server_metrics: dict[str, Any] = {}
    playback_stream: sd.RawOutputStream | None = None
    wav_file: wave.Wave_write | None = None

    print(f"[connect] {args.url}")
    print(f"[output] {output_path}")
    print(f"[playback] {'enabled' if args.play else 'disabled'}")

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
                f"{(connected_at - client_started_at) * 1000:.2f} ms"
            )

            await websocket.send(json.dumps(payload))
            request_sent_at = time.perf_counter()

            async for message in websocket:
                if isinstance(message, str):
                    event = json.loads(message)
                    event_type = event.get("type", "unknown")

                    print(
                        f"[{event_type}] "
                        f"{json.dumps(event, ensure_ascii=False)}"
                    )

                    if event_type == "accepted":
                        sample_rate = int(
                            event.get("sample_rate", DEFAULT_SAMPLE_RATE)
                        )
                        channels = int(event.get("channels", DEFAULT_CHANNELS))

                        wav_file = wave.open(str(output_path), "wb")
                        wav_file.setnchannels(channels)
                        wav_file.setsampwidth(SAMPLE_WIDTH_BYTES)
                        wav_file.setframerate(sample_rate)

                        if args.play:
                            playback_stream = sd.RawOutputStream(
                                samplerate=sample_rate,
                                channels=channels,
                                dtype="int16",
                                blocksize=0,
                                latency=args.playback_latency,
                            )
                            playback_stream.start()

                            print(
                                "[audio-device] "
                                f"sample_rate={sample_rate}, "
                                f"channels={channels}, dtype=int16"
                            )

                    elif event_type == "ttfa":
                        server_metrics.update(event)

                    elif event_type == "done":
                        server_metrics.update(event)
                        done_at = time.perf_counter()
                        completed = True

                    elif event_type == "error":
                        raise RuntimeError(
                            event.get("message", "Unknown server error")
                        )

                    continue

                received_binary_bytes += len(message)

                pcm = extract_pcm(message)
                pcm = align_pcm_frames(pcm, channels)

                if not pcm:
                    continue

                if wav_file is None:
                    wav_file = wave.open(str(output_path), "wb")
                    wav_file.setnchannels(channels)
                    wav_file.setsampwidth(SAMPLE_WIDTH_BYTES)
                    wav_file.setframerate(sample_rate)

                if first_pcm_at is None:
                    first_pcm_at = time.perf_counter()

                    if request_sent_at is not None:
                        print(
                            "[client-ttfa] "
                            f"{(first_pcm_at - request_sent_at) * 1000:.2f} ms"
                        )

                    print(
                        "[end-to-end-ttfa] "
                        f"{(first_pcm_at - client_started_at) * 1000:.2f} ms"
                    )

                wav_file.writeframesraw(pcm)
                saved_pcm_bytes += len(pcm)
                audio_chunks += 1

                if args.play:
                    if playback_stream is None:
                        playback_stream = sd.RawOutputStream(
                            samplerate=sample_rate,
                            channels=channels,
                            dtype="int16",
                            blocksize=0,
                            latency=args.playback_latency,
                        )
                        playback_stream.start()

                    await asyncio.to_thread(playback_stream.write, pcm)
                    played_pcm_bytes += len(pcm)

        if playback_stream is not None:
            await asyncio.to_thread(playback_stream.stop)
            playback_stream.close()
            playback_stream = None

        if wav_file is not None:
            wav_file.close()
            wav_file = None

    except Exception:
        if playback_stream is not None:
            try:
                playback_stream.abort()
                playback_stream.close()
            except Exception:
                pass

        if wav_file is not None:
            try:
                wav_file.close()
            except Exception:
                pass

        raise

    if not completed:
        raise RuntimeError(
            "WebSocket closed before the server sent the done event."
        )

    if request_sent_at is None:
        raise RuntimeError("Request timing was not initialized.")

    if done_at is None:
        done_at = time.perf_counter()

    if not output_path.exists():
        raise RuntimeError("No WAV file was created.")

    if saved_pcm_bytes == 0:
        raise RuntimeError(
            "The server sent no playable PCM audio. "
            "Check the server logs and WebSocket events."
        )

    connection_latency_ms = (
        (connected_at - client_started_at) * 1000
        if connected_at is not None
        else None
    )

    client_ttfa_ms = (
        (first_pcm_at - request_sent_at) * 1000
        if first_pcm_at is not None
        else None
    )

    end_to_end_ttfa_ms = (
        (first_pcm_at - client_started_at) * 1000
        if first_pcm_at is not None
        else None
    )

    client_total_latency_ms = (done_at - request_sent_at) * 1000
    end_to_end_latency_ms = (done_at - client_started_at) * 1000

    print()
    print("=" * 62)
    print("LATENCY SUMMARY")
    print("=" * 62)

    print_metric("Connection latency", connection_latency_ms)
    print_metric("Client TTFA", client_ttfa_ms)
    print_metric("End-to-end TTFA", end_to_end_ttfa_ms)
    print_metric("Server TTFA", server_metrics.get("server_ttfa_ms"))
    print_metric("Inference TTFA", server_metrics.get("inference_ttfa_ms"))
    print_metric("Client total latency", client_total_latency_ms)
    print_metric("End-to-end latency", end_to_end_latency_ms)
    print_metric(
        "Server total latency",
        server_metrics.get("server_total_latency_ms"),
    )
    print_metric(
        "Inference latency",
        server_metrics.get("inference_latency_ms"),
    )

    print("=" * 62)
    print(f"Saved WAV                    : {output_path}")
    print(f"Received binary bytes        : {received_binary_bytes:,}")
    print(f"Saved PCM bytes              : {saved_pcm_bytes:,}")
    print(f"Played PCM bytes             : {played_pcm_bytes:,}")
    print(f"Audio chunks                 : {audio_chunks}")
    print(f"Sample rate                  : {sample_rate} Hz")
    print(f"Channels                     : {channels}")
    print("=" * 62)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fish Speech WebSocket client with simultaneous "
            "playback, WAV saving, and latency reporting"
        )
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
    parser.add_argument(
        "--playback-latency",
        choices=["low", "high"],
        default="low",
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
            "Run this to inspect available playback devices:\n"
            'python -c "import sounddevice as sd; print(sd.query_devices())"',
            file=sys.stderr,
        )
        raise SystemExit(1)

    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
