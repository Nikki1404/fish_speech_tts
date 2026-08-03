# Fish Speech S2 Pro — Docker WebSocket App

A complete self-hosted project for the current open-source **Fish Audio S2 Pro** model. It runs the official Fish Speech HTTP server in one container and a lightweight FastAPI WebSocket gateway in a second container.

## Architecture

```text
Python WebSocket client
        |
        | ws://HOST:8880/ws/tts
        v
FastAPI WebSocket gateway
        |
        | POST http://fish-speech:8080/v1/tts
        v
Official Fish Speech server
        |
        v
fishaudio/s2-pro checkpoints
```

The gateway sends JSON control events and binary WAV chunks. The client patches the streamed WAV header sizes after completion so the saved file is valid in ordinary audio players:

1. `accepted`
2. `metadata`
3. `ttfa`
4. Binary WAV chunks
5. `done`

## Requirements

Recommended:

- Linux x86_64
- NVIDIA GPU with at least 24 GB VRAM for S2 Pro
- Recent NVIDIA driver
- NVIDIA Container Toolkit
- Docker Engine and Docker Compose v2
- Enough disk space for the Docker image and S2 Pro weights

CPU mode is included for functional testing, but S2 Pro will be extremely slow on CPU.

## 1. Configure

```bash
cp .env.example .env
```

The default upstream model-server image is:

```text
fishaudio/fish-speech:server-cuda
```

`Dockerfile.fish` derives from that official image and applies one narrow streaming fix: it suppresses the duplicate final waveform after the server has already emitted all PCM segments. Non-streaming output is unchanged.

The model repository is:

```text
fishaudio/s2-pro
```

## 2. Verify Docker GPU access

```bash
./scripts/check_gpu.sh
```

## 3. Download S2 Pro weights

The model is downloaded using a small Docker downloader, so no host Python setup is needed:

```bash
./scripts/download_model.sh
```

Expected paths:

```text
checkpoints/s2-pro/
checkpoints/s2-pro/codec.pth
```

## 4. Start the app

```bash
./scripts/start.sh
```

Or directly:

```bash
docker compose up --build
```

Health check:

```bash
curl http://127.0.0.1:8880/health
```

The Fish Speech model container is intentionally not exposed publicly. Only the WebSocket gateway is published.

## 5. Run the Python WebSocket client

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-client.txt
```

Generate audio:

```bash
python client/ws_client.py \
  --text "[professional broadcast tone] Welcome to Fish Audio S2 Pro." \
  --output output/demo.wav
```

Play after generation:

```bash
python client/ws_client.py \
  --text "[excited] This is a real-time WebSocket test!" \
  --output output/excited.wav \
  --play
```

For a remote machine:

```bash
python client/ws_client.py \
  --url ws://SERVER_IP:8880/ws/tts \
  --text "Hello from a remote client." \
  --output output/remote.wav
```

## Request schema

```json
{
  "text": "[whisper] This is a test.",
  "reference_id": null,
  "chunk_length": 200,
  "format": "wav",
  "latency": "normal",
  "seed": null,
  "use_memory_cache": "off",
  "normalize": true,
  "streaming": true,
  "max_new_tokens": 1024,
  "top_p": 0.8,
  "repetition_penalty": 1.1,
  "temperature": 0.8
}
```

Important: the self-hosted Fish Speech API does not currently expose a numeric `speed` parameter. Use S2 natural-language inline controls such as `[speak slowly]`, `[fast-paced]`, `[whisper]`, or `[professional broadcast tone]` instead.

## Reference voice / voice cloning

Use only audio you own or are authorized to use. A reference ID is a directory under `references/` containing an audio file and a same-name `.lab` transcript file.

Create it with the helper:

```bash
python client/reference_voice.py \
  --id my_voice \
  --audio /path/to/reference.wav \
  --text "Exact words spoken in the reference recording."
```

This creates:

```text
references/my_voice/sample.wav
references/my_voice/sample.lab
```

Then synthesize:

```bash
python client/ws_client.py \
  --reference-id my_voice \
  --memory-cache on \
  --text "[warm and friendly] This uses the authorized reference voice." \
  --output output/my_voice.wav
```

A clean, single-speaker reference of roughly 10–30 seconds generally works best.

## Optional API key

Set this in `.env`:

```text
WS_API_KEY=replace-with-a-strong-secret
```

Then call:

```bash
python client/ws_client.py \
  --api-key replace-with-a-strong-secret \
  --text "Authenticated request."
```

## CPU mode

```bash
docker compose -f docker-compose.cpu.yml up --build
```

This is not recommended for normal S2 Pro use.

## Logs

```bash
docker compose logs -f fish-speech
docker compose logs -f gateway
```

## Stop

```bash
docker compose down
```

## Update to the newest official image

```bash
docker compose build --pull fish-speech
docker compose up -d --build
```

For reproducible production deployments, replace `server-cuda` in `.env` with a tested versioned tag or immutable image digest.

## Local gateway smoke test without the model

This validates the WebSocket protocol using a mock Fish Speech HTTP server:

```bash
python3 -m venv .test-venv
source .test-venv/bin/activate
pip install -r requirements.txt -r requirements-client.txt
python tests/smoke_test.py
```

## License

Fish Speech code and S2 Pro weights use the Fish Audio Research License. Review the official license before deployment, especially for commercial use.
