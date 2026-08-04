from __future__ import annotations

import argparse
import asyncio
import json
import struct
import sys
import time
from pathlib import Path
from typing import Any

import sounddevice as sd
import websockets


DEFAULT_URL = "ws://127.0.0.1:8000/ws/tts"
DEFAULT_SAMPLE_RATE = 44100
DEFAULT_CHANNELS = 1
DEFAULT_SAMPLE_WIDTH = 2  # PCM16 = 2 bytes


def finalize_wav(path: Path) -> None:
    """
    Update RIFF and data sizes after streaming completes.
    """
    file_size = path.stat().st_size

    if file_size < 44:
        raise RuntimeError(
            f"Output is too small to be WAV audio: {file_size} bytes"
        )

    with path.open("r+b") as file:
        header = file.read(12)

        if header[:4] != b"RIFF" or header[8:12] != b"WAVE":
            raise RuntimeError("Output does not contain a valid WAV header.")

        # RIFF chunk size = complete file size - 8 bytes.
        file.seek(4)
        file.write(struct.pack("<I", file_size - 8))

        file.seek(0)
        content = file.read()

        data_position = content.find(b"data")

        if data_position < 0:
            raise RuntimeError("WAV data chunk was not found.")

        audio_start = data_position + 8
        audio_size = file_size - audio_start

        file.seek(data_position + 4)
        file.write(struct.pack("<I", audio_size))


def extract_pcm_from_wav_chunk(chunk: bytes) -> bytes:
    """
    If the chunk contains a WAV header, return only bytes after the data header.

    Normal PCM chunks are returned unchanged.
    """
    if not chunk.startswith(b"RIFF"):
        return chunk

    data_position = chunk.find(b"data")

    if data_position < 0:
        # This is probably only a partial/header chunk.
        return b""

    audio_start = data_position + 8

    if audio_start >= len(chunk):
        return b""

    return chunk[audio_start:]


def trim_incomplete_pcm_frame(
    pcm: bytes,
    channels: int,
    sample_width: int = DEFAULT_SAMPLE_WIDTH,
) -> bytes:
    """
    Ensure the audio buffer contains complete PCM frames.
    """
    frame_size = channels * sample_width

    if frame_size <= 0:
        return b""

    usable_size = len(pcm) - (len(pcm) % frame_size)
    return pcm[:usable_size]


def print_metric(
    label: str,
    value: float | int | None,
) -> None:
    if value is None:
        print(f"{label:<30}: N/A")
    else:
        print(f"{label:<30}: {float(value):.2f} ms")


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

    process_started_at = time.perf_counter()
    connected_at: float | None = None
    request_sent_at: float | None = None
    first_audio_at: float | None = None
    done_received_at: float | None = None

    sample_rate = DEFAULT_SAMPLE_RATE
    channels = DEFAULT_CHANNELS

    bytes_received = 0
    pcm_bytes_played = 0
    chunks_received = 0
    completed = False

    server_metrics: dict[str, Any] = {}

    audio_stream: sd.RawOutputStream | None = None

    print(f"[connect] {args.url}")
    print(f"[save] {output_path}")
    print(f"[live-playback] {'enabled' if args.play else 'disabled'}")

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

            with output_path.open("wb") as output_file:
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
                                event.get(
                                    "sample_rate",
                                    DEFAULT_SAMPLE_RATE,
                                )
                            )
                            channels = int(event.get("channels", 1))

                            if args.play and audio_stream is None:
                                audio_stream = sd.RawOutputStream(
                                    samplerate=sample_rate,
                                    channels=channels,
                                    dtype="int16",
                                    blocksize=0,
                                    latency=args.playback_latency,
                                )
                                audio_stream.start()

                                print(
                                    "[audio-device] "
                                    f"sample_rate={sample_rate}, "
                                    f"channels={channels}, "
                                    "dtype=int16"
                                )

                        elif event_type == "ttfa":
                            server_metrics.update(event)

                        elif event_type == "done":
                            server_metrics.update(event)
                            done_received_at = time.perf_counter()
                            completed = True

                        elif event_type == "error":
                            raise RuntimeError(
                                event.get(
                                    "message",
                                    "Unknown server error",
                                )
                            )

                        continue

                    # Save the complete stream, including the WAV header.
                    output_file.write(message)
                    output_file.flush()

                    bytes_received += len(message)
                    chunks_received += 1

                    pcm = extract_pcm_from_wav_chunk(message)
                    pcm = trim_incomplete_pcm_frame(
                        pcm,
                        channels=channels,
                    )

                    # Do not count a header-only chunk as first playable audio.
                    if pcm and first_audio_at is None:
                        first_audio_at = time.perf_counter()

                        if request_sent_at is not None:
                            print(
                                "[client-ttfa] "
                                f"{(first_audio_at - request_sent_at) * 1000:.2f} ms"
                            )

                        print(
                            "[end-to-end-ttfa] "
                            f"{(first_audio_at - process_started_at) * 1000:.2f} ms"
                        )

                    if args.play and pcm:
                        if audio_stream is None:
                            audio_stream = sd.RawOutputStream(
                                samplerate=sample_rate,
                                channels=channels,
                                dtype="int16",
                                blocksize=0,
                                latency=args.playback_latency,
                            )
                            audio_stream.start()

                        # Playback is blocking, so move it off the asyncio loop.
                        await asyncio.to_thread(audio_stream.write, pcm)
                        pcm_bytes_played += len(pcm)

        if audio_stream is not None:
            # Wait until queued audio has been played.
            await asyncio.to_thread(audio_stream.stop)
            audio_stream.close()
            audio_stream = None

    except Exception:
        if audio_stream is not None:
            try:
                audio_stream.abort()
                audio_stream.close()
            except Exception:
                pass

        if output_path.exists() and output_path.stat().st_size == 0:
            output_path.unlink()

        raise

    if not completed:
        raise RuntimeError(
            "WebSocket closed before the done event was received."
        )

    if request_sent_at is None:
        raise RuntimeError("Request start time was not recorded.")

    if done_received_at is None:
        done_received_at = time.perf_counter()

    finalize_wav(output_path)

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

    print()
    print("=" * 62)
    print("LATENCY SUMMARY")
    print("=" * 62)

    print_metric("Connection latency", connection_latency_ms)
    print_metric("Client TTFA", client_ttfa_ms)
    print_metric("End-to-end TTFA", end_to_end_ttfa_ms)

    print_metric(
        "Server TTFA",
        server_metrics.get("server_ttfa_ms"),
    )
    print_metric(
        "Inference TTFA",
        server_metrics.get("inference_ttfa_ms"),
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
        server_metrics.get("server_total_latency_ms"),
    )
    print_metric(
        "Inference latency",
        server_metrics.get("inference_latency_ms"),
    )

    print("=" * 62)
    print(f"Saved WAV                    : {output_path}")
    print(f"Received bytes               : {bytes_received:,}")
    print(f"Played PCM bytes             : {pcm_bytes_played:,}")
    print(f"Received chunks              : {chunks_received}")
    print(f"Sample rate                  : {sample_rate} Hz")
    print(f"Channels                     : {channels}")
    print("=" * 62)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Fish Speech WebSocket client with simultaneous "
            "streaming playback and WAV saving"
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
        help="Sounddevice playback latency setting",
    )

    playback_group = parser.add_mutually_exclusive_group()

    playback_group.add_argument(
        "--play",
        dest="play",
        action="store_true",
        help="Play audio while receiving and saving it",
    )

    playback_group.add_argument(
        "--no-play",
        dest="play",
        action="store_false",
        help="Save audio without live playback",
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
            "Check available devices with:\n"
            'python -c "import sounddevice as sd; print(sd.query_devices())"',
            file=sys.stderr,
        )
        raise SystemExit(1)

    except Exception as exc:
        print(f"[error] {exc}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
