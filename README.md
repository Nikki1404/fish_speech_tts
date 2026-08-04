# Fish Speech S2 Pro: one FastAPI server

One process and one port:

- `POST http://localhost:8000/v1/tts`
- `WS ws://localhost:8000/ws/tts`
- `GET http://localhost:8000/health`

## Build

```bash
DOCKER_BUILDKIT=1 docker build --progress=plain -t fish-s2-one-api:latest .
```

## Run

```bash
docker run --rm \
  --name fish-s2-one-api \
  --gpus all \
  --shm-size=8g \
  -p 8000:8000 \
  -e COMPILE=0 \
  fish-s2-one-api:latest
```

## Health

```bash
curl http://127.0.0.1:8000/health
```

## HTTP TTS

```bash
curl -X POST http://127.0.0.1:8000/v1/tts \
  -H 'Content-Type: application/json' \
  -d '{
    "text":"[professional broadcast tone] Hello from Fish Speech S2 Pro.",
    "format":"wav",
    "streaming":false,
    "chunk_length":200,
    "temperature":0.8,
    "top_p":0.8,
    "repetition_penalty":1.1
  }' \
  --output http-output.wav
```

## Local WebSocket client

```bash
python3 -m venv .client-venv
source .client-venv/bin/activate
pip install -r requirements-client.txt

python client.py \
  --url ws://127.0.0.1:8000/ws/tts \
  --text "[excited] This is streamed from one FastAPI server." \
  --output websocket-output.wav \
  --play
```
