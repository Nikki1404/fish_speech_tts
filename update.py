(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# nproc
free -h
df -h /

DOCKER_BUILDKIT=1 docker build \
  --progress=plain \
  -t fish-s2-cpu:latest \

docker run -d --cpus=12 --shm-size=8g -p 8000:8000 -e DEVICE=cpu -e OMP_NUM_THREADS=12 -e MKL_NUM_THREADS=12 -e OPENBLAS_NUM_THREADS=12 fish-s2-cpu:latest

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=12 \
  --shm-size=8g \
  -p 8000:8000 \
  -e DEVICE=cpu \
  -e OMP_NUM_THREADS=12 \
  -e MKL_NUM_THREADS=12 \
  -e OPENBLAS_NUM_THREADS=12 \
  fish-s2-cpu:latest

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=16 \
  --memory=48g \
  --memory-swap=48g \
  --shm-size=16g \
  -p 8000:8000 \
  -e OMP_NUM_THREADS=16 \
  -e MKL_NUM_THREADS=16 \
  -e OPENBLAS_NUM_THREADS=16 \
  fish-s2-cpu:latest

docker run -d \
  --name fish-s2-cpu \
  --restart unless-stopped \
  --cpus=12 \
  --memory=32g \
  --memory-swap=32g \
  --shm-size=8g \
  -p 8000:8000 \
  -e OMP_NUM_THREADS=12 \
  -e MKL_NUM_THREADS=12 \
  -e OPENBLAS_NUM_THREADS=12 \
  fish-s2-cpu:latest



curl -X POST http://127.0.0.1:8000/v1/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello there.",
    "format": "wav",
    "streaming": false,
    "chunk_length": 100,
    "max_new_tokens": 256
  }' \
  --output cpu-http-test.wav




python3 -m venv .client-venv
source .client-venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements-client.txt



python client.py \
  --url ws://127.0.0.1:8000/ws/tts \
  --text "Hello there." \
  --max-new-tokens 256 \
  --output cpu-websocket-test.wav
