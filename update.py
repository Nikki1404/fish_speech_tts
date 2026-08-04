(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# nproc
free -h
df -h /

               total        used        free      shared  buff/cache   available
Mem:            30Gi        10Gi       4.2Gi       377Mi        16Gi        19Gi
Swap:             0B          0B          0B
Filesystem      Size  Used Avail Use% Mounted on
/dev/root       518G  441G   77G  86% /
DOCKER_BUILDKIT=1 docker build \
  --progress=plain \
  -t fish-s2-cpu:latest \

(base) root@EC03-E01-AICOE1:/home/CORP/re_nikitav/fish_speech_tts# DOCKER_BUILDKIT=1 docker build --progress=plain -t fish-s2-cpu:latest .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 1.43kB done
#1 DONE 0.0s

#2 [auth] docker/dockerfile:pull token for registry-1.docker.io
#2 DONE 0.0s

#3 resolve image config for docker-image://docker.io/docker/dockerfile:1.7
#3 DONE 0.3s

#4 docker-image://docker.io/docker/dockerfile:1.7@sha256:a57df69d0ea827fb7266491f2813635de6f17269be881f696fbfdf2d83dda33e
#4 CACHED

#5 [internal] load metadata for docker.io/fishaudio/fish-speech:latest-server-cpu
#5 ERROR: docker.io/fishaudio/fish-speech:latest-server-cpu: not found

#6 [auth] fishaudio/fish-speech:pull token for registry-1.docker.io
#6 DONE 0.0s
------
 > [internal] load metadata for docker.io/fishaudio/fish-speech:latest-server-cpu:
------
Dockerfile:3
--------------------
   1 |     # syntax=docker/dockerfile:1.7
   2 |
   3 | >>> FROM fishaudio/fish-speech:latest-server-cpu
   4 |
   5 |     ENV http_proxy="http://163.116.128.80:8080"
--------------------
ERROR: failed to build: failed to solve: fishaudio/fish-speech:latest-server-cpu: docker.io/fishaudio/fish-speech:latest-server-cpu: not found
  .

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
