(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# nproc
free -h
df -h /

DOCKER_BUILDKIT=1 docker build \
  --progress=plain \
  -t fish-s2-cpu:latest \

docker run -d --shm-size=8g -p 8000:8000 -e DEVICE=cpu  fish-s2-cpu:latest
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# docker logs a53f4b64b248
[2026-08-04 10:25:41] Starting Fish Speech API Server...
[2026-08-04 10:25:41] Device args: --device cpu
[2026-08-04 10:25:41] Compile args: uvicorn app.main:app --host 0.0.0.0 --port 8000
[2026-08-04 10:25:41] Server: 0.0.0.0:8080
   Building fish-speech @ file:///app
      Built fish-speech @ file:///app
Uninstalled 1 package in 15ms
Installed 1 package in 3ms
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:44: SyntaxWarning: invalid escape sequence '\_'
  Type of window to use, by default ``sqrt\_hann``.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1014: SyntaxWarning: invalid escape sequence '\_'
  using functools.lru\_cache.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1092: SyntaxWarning: invalid escape sequence '\_'
  """Compute how the STFT should be padded, based on match\_stride.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1141: SyntaxWarning: invalid escape sequence '\_'
  Type of window to use, by default ``sqrt\_hann``.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1222: SyntaxWarning: invalid escape sequence '\_'
  """Computes inverse STFT and sets it to audio\_data.
/app/.venv/lib/python3.12/site-packages/torch/amp/autocast_mode.py:266: UserWarning: User provided device_type of 'cuda', but CUDA is not available. Disabling
  warnings.warn(
usage: api_server.py [-h] [--mode {tts}]
                     [--llama-checkpoint-path LLAMA_CHECKPOINT_PATH]
                     [--decoder-checkpoint-path DECODER_CHECKPOINT_PATH]
                     [--decoder-config-name DECODER_CONFIG_NAME]
                     [--device DEVICE] [--half] [--compile]
                     [--max-text-length MAX_TEXT_LENGTH] [--listen LISTEN]
                     [--workers WORKERS] [--api-key API_KEY]
api_server.py: error: unrecognized arguments: uvicorn app.main:app --host 0.0.0.0 --port 8000
(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# docker logs a53f4b64b248
[2026-08-04 10:25:41] Starting Fish Speech API Server...
[2026-08-04 10:25:41] Device args: --device cpu
[2026-08-04 10:25:41] Compile args: uvicorn app.main:app --host 0.0.0.0 --port 8000
[2026-08-04 10:25:41] Server: 0.0.0.0:8080
   Building fish-speech @ file:///app
      Built fish-speech @ file:///app
Uninstalled 1 package in 15ms
Installed 1 package in 3ms
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:44: SyntaxWarning: invalid escape sequence '\_'
  Type of window to use, by default ``sqrt\_hann``.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1014: SyntaxWarning: invalid escape sequence '\_'
  using functools.lru\_cache.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1092: SyntaxWarning: invalid escape sequence '\_'
  """Compute how the STFT should be padded, based on match\_stride.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1141: SyntaxWarning: invalid escape sequence '\_'
  Type of window to use, by default ``sqrt\_hann``.
/app/.venv/lib/python3.12/site-packages/audiotools/core/audio_signal.py:1222: SyntaxWarning: invalid escape sequence '\_'
  """Computes inverse STFT and sets it to audio\_data.
/app/.venv/lib/python3.12/site-packages/torch/amp/autocast_mode.py:266: UserWarning: User provided device_type of 'cuda', but CUDA is not available. Disabling
  warnings.warn(
usage: api_server.py [-h] [--mode {tts}]
                     [--llama-checkpoint-path LLAMA_CHECKPOINT_PATH]
                     [--decoder-checkpoint-path DECODER_CHECKPOINT_PATH]
                     [--decoder-config-name DECODER_CONFIG_NAME]
                     [--device DEVICE] [--half] [--compile]
                     [--max-text-length MAX_TEXT_LENGTH] [--listen LISTEN]
                     [--workers WORKERS] [--api-key API_KEY]
api_server.py: error: unrecognized arguments: uvicorn app.main:app --host 0.0.0.0 --port 8000


Run 'docker run --help' for more information
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
